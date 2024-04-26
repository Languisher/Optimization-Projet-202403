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
        delta_v = acceleration * (self.distance_step / max(self.vehicle.velocity, 5)) * 1000  # prevent division by zero
        new_velocity = max(min(self.vehicle.velocity + delta_v, self.vehicle.velocity_max),
                           self.min_velocity)  # use a min_velocity attribute

        # Energy updates (assuming all powers are in Watts and all times are in seconds)
        power_consumed = output_power * (self.distance_step / max(self.vehicle.velocity, 5)) 
        # power_consumed = self.vehicle.output_power

        power_regenerated = -0.740 * self.vehicle.velocity * (
                    self.distance_step / max(self.vehicle.velocity, 5)) 

        new_energy = max(self.vehicle.energy_left - power_consumed + power_regenerated, 0)

        # Update distance and time
        new_distance = self.vehicle.covered_distance + self.distance_step
        delta_t = self.distance_step / max(self.vehicle.velocity, 5) * 3600  # to convert hours to seconds
        new_time = self.time_list[-1] + delta_t

        # Update vehicle state and lists
        self.vehicle.update_velocity(new_velocity)
        self.vehicle.energy_left = new_energy 
        self.vehicle.covered_distance = new_distance

        self.velocity_list.append(new_velocity)
        self.energy_list.append(new_energy)
        self.distance_list.append(new_distance)
        self.time_list.append(new_time)
        self.output_power_list.append(np.abs(output_power / 1000))  # Convert watts to kilowatts for recording

    def calculate_possible_output_power_value(self, incline_angle, mu):
        velocity = self.vehicle.velocity
        rad_angle = np.radians(incline_angle)
        u1 = 0
        u2 = 9000
        u3 = 60000
        u4 = self.vehicle.mass * self.g * velocity*(np.sin(rad_angle) + mu * np.cos(rad_angle)) - self.C_d * self.A * velocity ** 2 / 21.15
        u4 = np.abs(u4)
        return [u1, u2, u3, u4 / 1000]

    def power_strategy(self, output_values):
        output_u = np.random.choice(output_values)
        return output_u


    def simulate(self):
        self.initialize_state_lists()
        for distance, incline_angle, mu in self.route.road_info_list:
            # print(f"Road: {distance}, incli: {incline_angle}, mu: {mu}")
            possible_output_values = self.calculate_possible_output_power_value(incline_angle, mu)
            self.vehicle.output_power = self.power_strategy(possible_output_values)
            # print(self.vehicle.output_power)
            self.update_vehicle_state(incline_angle, self.vehicle.output_power, mu)

            if self.vehicle.velocity < self.min_velocity:
                self.vehicle.velocity = self.min_velocity

            if self.vehicle.energy_left < 2:
                break

    def plot_results(self):
        plt.figure(figsize=(12, 8))

        plt.subplot(4, 1, 1)
        plt.plot(self.distance_list, self.time_list, label='Time (s)')
        plt.xlabel('Distance (km)')
        plt.ylabel('Time (s)')
        plt.legend()

        plt.subplot(4, 1, 2)
        plt.stem(self.distance_list, self.output_power_list, label='Power Output (kW)')
        plt.xlabel('Distance (km)')
        plt.ylabel('Power Output (kW)')
        plt.legend()

        plt.subplot(4, 1, 3)
        plt.plot(self.distance_list, self.velocity_list, label='Velocity (km/h)')
        plt.xlabel('Distance (km)')
        plt.ylabel('Velocity (km/h)')
        plt.legend()

        plt.subplot(4, 1, 4)
        plt.plot(self.distance_list, self.energy_list, label='Energy (kJ)')
        plt.xlabel('Distance (km)')
        plt.ylabel('Energy (kJ)')
        plt.legend()

        plt.tight_layout()
        plt.show()
