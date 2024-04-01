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
        self.CP = 50  # Watts, Critical Power

        self.calculate_adjusted_power = lambda power_input: 0.0772 * power_input \
                                                            + 222.49

        # Initialize co-state variables, which will need to be adjusted based on your problem
        self.lambda_position = 0  # Co-state variable associated with the position
        self.lambda_velocity = 0  # Co-state variable associated with the velocity
        self.lambda_awc = 0       # Co-state variable associated with the AWC                                                 

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

    def calculate_hamiltonian(self, power_output):
        """
        Placeholder for the Hamiltonian calculation. This function should return the value of the Hamiltonian.
        It should incorporate the dynamics of the system, the cost function, and the co-state variables.
        """
        # Example: H = L(x, u, t) + lambda^T * f(x, u, t)
        # You will need to define L and f based on your specific problem

        # Calculate total resistive forces as done in change_velocity
        drag_force = 0.5 * self.Cd * self.A * self.rho * self.velocity ** 2
        rolling_resistance_force = self.CR * self.mass * self.g * np.cos(np.arctan(self.slope))
        gravity_force = self.mass * self.g * np.sin(np.arctan(self.slope))
        total_resistive_force = drag_force + rolling_resistance_force + gravity_force
        
        # Assuming adjustment = 1 for power_output > CP, else 0
        adjustment = 1 if power_output > self.CP else 0
        
        # Hamiltonian calculation
        H = self.lambda_position * (power_output - self.CP) ** 2 if power_output > self.CP else 0
        H += self.lambda_velocity * ((power_output - total_resistive_force * self.velocity) / self.mass)
        H += self.lambda_awc * adjustment * (power_output - self.CP)
        return H


    def update_co_states(self, dt):
        """
        Placeholder for updating the co-state variables. This will require solving the system of
        ODEs that describe the evolution of the co-state variables over time.
        """
        # Example: lambda_dot = -dH/dx
        # The specific implementation will depend on the partial derivatives of your Hamiltonian
        self.lambda_position -= dt * self.partial_derivative_hamiltonian_position()
        self.lambda_velocity -= dt * self.partial_derivative_hamiltonian_velocity()
        self.lambda_awc -= dt * self.partial_derivative_hamiltonian_awc()

    def partial_derivative_hamiltonian_position(self):
        # Placeholder for partial derivative of Hamiltonian with respect to position
        return 0  # Replace with the actual calculation

    def partial_derivative_hamiltonian_velocity(self):
        # Simplified derivative with respect to velocity
        drag_force_derivative = self.Cd * self.A * self.rho * self.velocity
        return -self.lambda_velocity * drag_force_derivative / self.mass


    def partial_derivative_hamiltonian_awc(self):
        # Placeholder for partial derivative of Hamiltonian with respect to AWC
        return 0  # Replace with the actual calculation

    def find_optimal_control(self):
        """
        Placeholder for finding the optimal control that minimizes the Hamiltonian.
        This may require solving an optimization problem at each time step.
        """
        # This is a complex problem that generally requires numerical methods to solve.
        # Here we simply return a placeholder value.
        optimal_power_output = self.CP  # Replace with logic to find the optimal control
        return optimal_power_output


import numpy as np
import matplotlib.pyplot as plt

# Assuming CyclistState class definition remains the same

if __name__ == '__main__':
    cyclist = CyclistState(position=0, velocity=5, awc=20000)  # Initial state
    dt = 1  # Time step in seconds
    slope = 0.05  # Slope of the course (5% uphill)
    simulation_time = 60  # Simulate for 60 seconds

    positions = []
    velocities = []
    awcs = []
    times = np.arange(0, simulation_time + dt, dt)

    for t in times:
        # Store current state
        positions.append(cyclist.position)
        velocities.append(cyclist.velocity)
        awcs.append(cyclist.awc)

        # Simulate changes for the current timestep
        power_output = cyclist.find_optimal_control()  # Find the optimal power output
        cyclist.change_velocity(power_output, slope, dt)
        cyclist.change_awc(power_output, dt)
        cyclist.change_position(dt)

        # Update the co-state variables
        cyclist.update_co_states(dt)

    # Plotting
    fig, axs = plt.subplots(1, 2, figsize=(16, 8))
    
    axs[0].plot(times, positions)
    axs[0].set_title('Position over Time')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Position (m)')

    axs[1].plot(times, velocities)
    axs[1].set_title('Velocity over Time')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Velocity (m/s)')


    plt.tight_layout()
    plt.show()
