import numpy as np
import matplotlib.pyplot as plt

class Simulation:
    def __init__(self, vehicle, route):
        self.vehicle = vehicle
        self.route = route
        self.distance_step = 0.01

        # Physical constants
        self.g = 9.81  # Gravity acceleration in m/s^2
        self.C_d = 0.3  # Drag coefficient, consider moving to vehicle properties if it varies per vehicle
        self.A = self.vehicle.frontal_area  # Frontal area from vehicle
        self.rho = 1.225  # Air density in kg/m^3
        self.eta = 0.86   # Efficiency coef

        self.time_list = [0]  
        self.velocity_list = [vehicle.velocity] 
        self.energy_list = [vehicle.energy_left]  
        self.distance_list = [0]  
        self.output_power_list = [0]

    def update_vehicle_state(self, incline_angle, output_power, mu):
        current_velocity = self.vehicle.velocity
        current_energy = self.vehicle.energy_left
        current_distance = self.vehicle.covered_distance
        time = self.time_list[-1]

        # Convert angle to radians for computation
        rad_angle = incline_angle

        
        # Calculate forces
        gravity_force = self.vehicle.mass * self.g * np.sin(rad_angle)
        friction_force = self.vehicle.mass * self.g * np.cos(rad_angle) * mu
        drag_force = 0.5 * self.C_d * self.A * self.rho * current_velocity**2

        # Calculate acceleration
        total_force = output_power / current_velocity - gravity_force - friction_force - drag_force
        acceleration = total_force / self.vehicle.mass * 1000

        # Velocity update
        delta_v = acceleration * (self.distance_step / current_velocity)
        new_velocity = max(min(current_velocity + delta_v, self.vehicle.velocity_max), 0)

        # Energy update
        power_consumed = 1/(3.6 * self.eta) * (mu * self.vehicle.mass * self.g + 1/2 * self.rho * self.C_d * self.A * self.vehicle.velocity ** 2) * self.vehicle.velocity
        power_regenerated = (0.740 * self.vehicle.velocity + 1.8) * 1000
        
        delta_energy_consumption = power_consumed * (self.distance_step / current_velocity)
        delta_energy_regeneration = power_regenerated * (self.distance_step / current_velocity)

        new_energy = max(current_energy - delta_energy_consumption + delta_energy_regeneration, 0)

        # Distance update
        new_distance = current_distance + self.distance_step

        # Time update
        delta_t = self.distance_step / current_velocity
        new_time = time + delta_t

        # Update vehicle and lists
        self.vehicle.update_velocity(new_velocity)  # Assuming a method exists
        self.vehicle.energy_left = new_energy
        self.vehicle.covered_distance = new_distance

        self.velocity_list.append(new_velocity)
        self.energy_list.append(new_energy)
        self.distance_list.append(new_distance)
        self.time_list.append(new_time)
        self.output_power_list.append(output_power)

    def power_strategy(self, vehicle):
        # raise NotImplementedError("Power strategy is not implemented.")
        return 150000

    def simulate(self):
        for distance, incline_angle, mu in zip(self.route.distance_list, self.route.inclination_angle_list, self.route.mu_list):
            num_steps = int(np.ceil(distance / self.distance_step))
            for _ in range(num_steps):
                print(self.vehicle)
                self.vehicle.output_power = self.power_strategy(self.vehicle)
                self.update_vehicle_state(incline_angle, self.vehicle.output_power, mu)
                
                if self.vehicle.velocity < 2:
                    self.vehicle.velocity = 2
                    
                if self.vehicle.energy_left < 2:
                    break

    def plot_results(self):
        plt.figure(figsize=(12, 8))

        plt.subplot(4, 1, 1)
        plt.plot(self.distance_list, self.time_list, label='Time (s)')
        plt.xlabel('Distance (m)')
        plt.ylabel('Time (s)')
        plt.legend()

        plt.subplot(4, 1, 2)
        plt.plot(self.distance_list, self.output_power_list, label='Power Output (W)')
        plt.xlabel('Distance (m)')
        plt.ylabel('Power Output (W)')
        plt.legend()

        plt.subplot(4, 1, 3)
        plt.plot(self.distance_list, self.velocity_list, label='Velocity (m/s)')
        plt.xlabel('Distance (m)')
        plt.ylabel('Velocity (km/h)')
        plt.legend()

        plt.subplot(4, 1, 4)
        plt.plot(self.distance_list, self.energy_list, label='Energy (J)')
        plt.xlabel('Distance (m)')
        plt.ylabel('Energy (J)')
        plt.legend()

        plt.tight_layout()
        plt.show()
