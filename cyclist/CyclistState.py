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
        self.slope = -90

        self.calculate_adjusted_power = lambda power_input: 0.0772 * power_input \
                                                            + 222.49

        # Initialize co-state variables, which will need to be adjusted based on your problem
        self.lambda_position = 0  # Co-state variable associated with the position
        self.lambda_velocity = 0  # Co-state variable associated with the velocity
        self.lambda_awc = 0       # Co-state variable associated with the AWC                                                 

    def change_position(self, dt=1):
        self.position += self.velocity * dt

    def change_velocity(self, power_output, slope=0, dt=1):
        if (self.velocity == 0):
            return

        if (slope):
            self.slope = slope
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
        Calculate the value of the Hamiltonian.
        It should incorporate the dynamics of the system, the cost function, and the co-state variables.
        """
        # Calculate total resistive forces as done in change_velocity
        drag_force = 0.5 * self.Cd * self.A * self.rho * self.velocity ** 2
        rolling_resistance_force = self.CR * self.mass * self.g * np.cos(self.slope)
        gravity_force = self.mass * self.g * np.sin(self.slope)
        total_resistive_force = drag_force + rolling_resistance_force + gravity_force

        # Assuming adjustment = 1 for power_output > CP, else 0
        adjustment = 1 if power_output > self.CP else 0
        
        # Update the dynamics (f) based on the state and control inputs
        # Here, the dynamics are the changes in position and velocity
        f_position = self.velocity
        f_velocity = (power_output - total_resistive_force) / self.mass
        
        # Define the Lagrangian L, which in this case can be the negative of power_output
        L = -power_output

        # Calculate the Hamiltonian
        H = self.lambda_position * f_position + self.lambda_velocity * f_velocity - L
        
        return H


    def update_co_states(self, dt):
        """
        Update the co-state variables using the Hamiltonian.
        """
        # Example: lambda_dot = -dH/dx
        # Here we need to compute the derivatives of the Hamiltonian with respect to the state variables

        # For illustrative purposes, we'll use very simple placeholders
        # The partial derivatives of the Hamiltonian with respect to position and velocity would depend on the system
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
        Find the optimal control that minimizes the Hamiltonian.
        This will typically involve setting the derivative of the Hamiltonian with respect to the control to zero.
        """
        # Placeholder for the optimal control strategy
        # This is typically found by setting the derivative of H with respect to the control (u) to zero.
        # However, since this can be complex, we might need to use a numerical solver.
        # For now, we will use a simple gradient descent or another optimization algorithm to find this.

        # Starting with the current power output as the initial guess
        current_power_output = self.CP

        # Define a small perturbation
        epsilon = 1e-4
        delta = 0.1

        # Compute the Hamiltonian for the current power output
        H_current = self.calculate_hamiltonian(current_power_output)

        # Compute the Hamiltonian for the power output plus a small perturbation
        H_perturbed = self.calculate_hamiltonian(current_power_output + epsilon)

        # Compute the gradient of the Hamiltonian with respect to the power output
        dH_dpower = (H_perturbed - H_current) / epsilon

        # Update the power output in the direction that decreases the Hamiltonian
        new_power_output = current_power_output - delta * dH_dpower

        # Ensure the new power output is within the allowed limits
        new_power_output = np.clip(new_power_output, 0, self.calculate_adjusted_power(new_power_output))

        return new_power_output


import numpy as np
import matplotlib.pyplot as plt

# Assuming CyclistState class definition remains the same

if __name__ == '__main__':
    cyclist = CyclistState(position=0, velocity=5, awc=20000)  # Initial state
    dt = 1  # Time step in seconds
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
        cyclist.change_velocity(power_output)
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
