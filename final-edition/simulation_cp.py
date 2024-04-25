import numpy as np
import matplotlib.pyplot as plt


class Simulation:
    def __init__(self, vehicle, route, distance_step=1, drag_coefficient=0.6, efficiency=0.86, gravity=9.81, min_velocity=2):
        """
        Initializes the Simulation with a given vehicle and route.

        Parameters:
        vehicle (Vehicle): The vehicle object containing vehicle-specific properties.
        route (Route): The route object containing information about the journey.

        Attributes:
        g (float): Acceleration due to gravity in m/s^2.
        C_d (float): Drag coefficient, which could be moved to vehicle properties if it varies per vehicle.
        A (float): Frontal area of the vehicle in m^2, sourced from the vehicle properties.
        eta (float): Efficiency coefficient, assuming constant efficiency across the simulation.
        time (int): Simulation time in seconds, initialized to 0.
        time_list (list of int): List to record time at each simulation step, starting at 0.
        distance_step (int): Distance increment for each simulation step in meters.
        distance_list (list of int): List to record the cumulative distance traveled.
        velocity_list (list of float): List to record the vehicle's velocity at each step.
        energy_list (list of float): List to record the vehicle's remaining energy.
        output_power_list (list of float): List to record the output power at each step.
        """

        if vehicle is None or route is None:
            raise ValueError("Vehicle and route cannot be None.")
        if distance_step <= 0:
            raise ValueError("Distance step must be positive.")
        if not (0 <= drag_coefficient <= 1):
            raise ValueError("Drag coefficient must be between 0 and 1.")
        if not (0 <= efficiency <= 1):
            raise ValueError("Efficiency must be between 0 and 1.")

        self.vehicle = vehicle
        self.route = route

        # Physical constants
        self.g = gravity
        self.C_d = drag_coefficient
        self.A = self.vehicle.frontal_area
        self.eta = efficiency
        self.min_velocity = min_velocity
        
        self.policy = None

        # We would record the current status and store them in a list container
        self.time = 0
        self.time_list = []

        self.distance_step = distance_step
        self.distance_list = []

        self.velocity_list = []
        self.energy_list = []
        self.output_power_list = []

        self.initialize_state_lists()

        

    def initialize_state_lists(self):
        self.time_list = [self.time]
        self.distance_list = [self.vehicle.covered_distance]
        self.velocity_list = [self.vehicle.velocity]
        self.energy_list = [self.vehicle.energy_left]
        self.output_power_list = [self.vehicle.output_power]

    def update_vehicle_state(self, incline_angle, output_power, mu):
        rad_angle = np.radians(incline_angle)  # Convert angle to radians

        # Calculate forces
        gravity_force = self.vehicle.mass * self.g * np.sin(rad_angle)
        friction_force = self.vehicle.mass * self.g * np.cos(rad_angle) * mu
        drag_force = self.C_d * self.A * self.vehicle.velocity ** 2 / 2  # Adjusted divisor based on typical air density and speed squared

        # Calculate acceleration
        total_force = output_power / self.vehicle.velocity - gravity_force - friction_force - drag_force
        acceleration = total_force / self.vehicle.mass

        # Update velocity
        delta_v = acceleration * (self.distance_step / max(self.vehicle.velocity, 0.1))  # prevent division by zero
        new_velocity = max(min(self.vehicle.velocity + delta_v, self.vehicle.velocity_max),
                           self.min_velocity)  # use a min_velocity attribute

        # Energy updates (assuming all powers are in Watts and all times are in seconds)
        # power_consumed = output_power * (self.distance_step / max(self.vehicle.velocity, 0.1))
        power_consumed = self.vehicle.output_power

        power_regenerated = -0.740 * self.vehicle.velocity * (
                    self.distance_step / max(self.vehicle.velocity, 0.1))  # assuming negative for regeneration

        new_energy = max(self.vehicle.energy_left - power_consumed + power_regenerated, 0)

        # Update distance and time
        new_distance = self.vehicle.covered_distance + self.distance_step
        delta_t = self.distance_step / max(self.vehicle.velocity, 0.1) * 3600  # to convert hours to seconds
        new_time = self.time_list[-1] + delta_t

        # Update vehicle state and lists
        self.vehicle.update_velocity(new_velocity)
        self.vehicle.energy_left = new_energy
        self.vehicle.covered_distance = new_distance

        self.velocity_list.append(new_velocity)
        self.energy_list.append(new_energy)
        self.distance_list.append(new_distance)
        self.time_list.append(new_time)
        self.output_power_list.append(output_power / 1000)  # Convert watts to kilowatts for recording

        return new_velocity, new_energy, delta_t

    def possible_output_power_values(self, incline_angle, mu):
        rad_angle = np.radians(incline_angle)
        u1 = 0
        u2 = 9000
        u3 = 150000
        u4 = self.vehicle.mass * self.g * self.vehicle.velocity * (np.sin(rad_angle) + mu * np.cos(rad_angle)) - self.C_d * self.A * self.vehicle.velocity ** 2 / 21.15
        return [u1, u2, u3, u4]


    def dynamic_programming_approach(self):
        N = len(self.route.distance_list)
        print(f"Length of self.distance_list: {len(self.distance_list)}")
        print(f"Value of N (number of route segments): {N}")
        J = np.full((N+1, 4), np.inf)  # Set initial costs to infinity


        # Backward pass to calculate the costs
        for i in range(N-1, -1, -1):
            # Print the current index and the lengths of the lists
            print(f"Current segment index: {i}")
            print(f"Length of self.distance_list: {len(self.distance_list)}")
            print(f"Length of self.velocity_list: {len(self.velocity_list)}")
            for j in range(4):
                possible_powers = self.possible_output_power_values(self.route.inclination_angle_list[i], self.route.mu_list[i])
                costs = []
                for power in possible_powers:
                    new_velocity, new_energy, _ = self.calculate_next_state(self.route.inclination_angle_list[i], power, self.route.mu_list[i])

                    if i == N-1:
                        # If it's the last segment, we use the last available distance value
                        delta_t = self.distance_list[-1] / max(new_velocity, self.min_velocity) * 3600
                    else:
                        # For all other segments, we use i+1
                        delta_t = self.distance_list[i+1] / max(new_velocity, self.min_velocity) * 3600

                    cost = delta_t if new_velocity > 0 else np.inf
                    costs.append(cost + J[i+1, j])
                J[i, j] = min(costs)

        # Forward pass to find the optimal policy
        policy = np.zeros(N)
        for i in range(N):
            min_cost, min_cost_index = min((cost, idx) for idx, cost in enumerate(J[i]))
            policy[i] = possible_powers[min_cost_index]
            self.update_vehicle_state(self.route.inclination_angle_list[i], policy[i], self.route.mu_list[i])

        # Store the policy
        self.policy = policy

        # Return policy as it might be needed elsewhere
        return policy

        
    def calculate_next_state(self, incline_angle, output_power, mu):
        rad_angle = np.radians(incline_angle)  # Convert angle to radians
        # Calculate forces based on current vehicle state
        gravity_force = self.vehicle.mass * self.g * np.sin(rad_angle)
        friction_force = self.vehicle.mass * self.g * np.cos(rad_angle) * mu
        drag_force = self.C_d * self.A * self.vehicle.velocity ** 2 / 2
        # Calculate acceleration and new velocity without updating vehicle state
        total_force = output_power / self.vehicle.velocity - gravity_force - friction_force - drag_force
        acceleration = total_force / self.vehicle.mass
        delta_v = acceleration * (self.distance_step / max(self.vehicle.velocity, self.min_velocity))
        new_velocity = max(min(self.vehicle.velocity + delta_v, self.vehicle.velocity_max), self.min_velocity)
        # Calculate new energy and cost time
        power_consumed = output_power * (self.distance_step / max(self.vehicle.velocity, self.min_velocity))
        power_regenerated = -0.740 * self.vehicle.velocity * (self.distance_step / max(self.vehicle.velocity, self.min_velocity))
        new_energy = max(self.vehicle.energy_left - power_consumed + power_regenerated, 0)
        delta_t = self.distance_step / max(self.vehicle.velocity, self.min_velocity)
        return new_velocity, new_energy, delta_t

    # You would call this method in your simulate method instead of the backward_pass and forward_pass
    def simulate(self):
        self.dynamic_programming_approach()
        self.plot_results()


    def plot_results(self):
        plt.figure(figsize=(12, 8))

        plt.subplot(4, 1, 1)
        plt.plot(self.distance_list, self.time_list, label='Time (s)')
        plt.xlabel('Distance (m)')
        plt.ylabel('Time (s)')
        plt.legend()

        plt.subplot(4, 1, 2)
        plt.stem(self.distance_list, self.output_power_list, label='Power Output (kW)')
        plt.xlabel('Distance (m)')
        plt.ylabel('Power Output (W)')
        plt.legend()

        plt.subplot(4, 1, 3)
        plt.plot(self.distance_list, self.velocity_list, label='Velocity (km/h)')
        plt.xlabel('Distance (m)')
        plt.ylabel('Velocity (m/s)')
        plt.legend()

        plt.subplot(4, 1, 4)
        plt.plot(self.distance_list, self.energy_list, label='Energy (kJ)')
        plt.xlabel('Distance (m)')
        plt.ylabel('Energy (J)')
        plt.legend()

        plt.tight_layout()
        plt.show()
