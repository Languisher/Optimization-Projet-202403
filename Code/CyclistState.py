import numpy as np


class CyclistState:
    def __init__(self, position=0, velocity=0, awc=0):
        self.position = position
        self.velocity = velocity
        self.awc = awc
        # Constants (You may adjust these based on real-world data or detailed models)
        self.mass = 70  # kg, mass of cyclist + bike
        self.g = 9.81  # m/s^2, acceleration due to gravity
        self.Cd = 0.3  # Aerodynamic drag coefficient
        self.A = 1  # Frontal area, in m^2
        self.rho = 1.225  # kg/m^3, air density at sea level
        self.CR = 0.005  # Coefficient of rolling resistance
        self.CP = 300  # Watts, Critical Power

        self.calculate_adjusted_power = lambda power_input: 0.0772 * power_input \
                                                            + 222.49

    def change_position(self, dt=1):
        self.position += self.velocity * dt

    def change_velocity(self, power_output, slope=0.05, dt=1):
        if (self.velocity == 0):
            return

        # Calculate total resistive forces
        drag_force = 0.5 * self.Cd * self.A * self.rho * self.velocity ** 2
        rolling_resistance_force = self.CR * self.mass * self.g * np.cos(slope)
        gravity_force = self.mass * self.g * np.sin(slope)
        total_resistive_force = drag_force + rolling_resistance_force + gravity_force

        # Net force applied
        net_force = power_output / self.velocity - total_resistive_force

        # Acceleration
        acceleration = net_force / self.mass

        # Update velocity
        self.velocity += acceleration * dt
        # Ensure velocity does not become negative
        self.velocity = max(0, self.velocity)

    def change_awc(self, power_output, dt=1):
        if power_output >= self.CP:
            # Deplete AWC based on the excess power and time
            self.awc -= (power_output - self.CP) * dt
        else:
            adjusted_power = self.calculate_adjusted_power(power_output)
            self.awc -= (adjusted_power - self.CP) * dt

        # Ensure AWC does not become negative
        self.awc = max(0, self.awc)


    def __str__(self):
        return (f"***** Current state *****\n"
                f"Position: {self.position} meters, \n"
                f"Velocity: {self.velocity} m/s, \n"
                f"AWC: {self.awc} Joules\n"
                f"**************************\n")


if __name__ == '__main__':
    cyclist = CyclistState(position=0, velocity=5, awc=20000)  # Initial state
    dt = 1  # Time step in seconds
    slope = 0.05  # Slope of the course (5% uphill)
    power_output = 350  # Power output in Watts

    # Simulate changes for a single timestep
    cyclist.change_position(dt)
    cyclist.change_velocity(power_output, slope, dt)
    cyclist.change_awc(power_output, dt)

    print(cyclist)
