import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Constants and Parameters (Need to be calibrated based on experimental data)
CP = 250  # Critical Power in Watts
AWC = 20000  # Anaerobic Work Capacity in Joules
m_b = 75  # Mass of the bicycle and rider in kilograms
m = m_b * 1.014  # Effective mass which is 1.4% greater than m_b
g = 9.81  # Gravitational acceleration in m/s^2
C_d = 0.63  # Aerodynamic drag coefficient
A = 0.509  # Frontal area in square meters
rho = 1.226  # Density of air in kg/m^3
C_R = 0.005  # Coefficient of rolling resistance

# Functions to compute the derivatives of the state variables
def f1(v):
    # This is a simple relation so we return v directly
    return v

def f2(u, v, theta):
    # Using Newton's second law to compute the derivative of velocity
    drag_force = 0.5 * C_d * A * rho * v**2
    rolling_resistance = C_R * g * np.cos(theta)
    gravitational_force = m_b * g * np.sin(theta)
    return (u - (gravitational_force + rolling_resistance + drag_force)) / (m * v)

def f3(u, w, recovery):
    # Energy expenditure and recovery dynamics
    if u >= CP:  # Above Critical Power, energy is being used
        return -(u - CP)
    else:  # Below Critical Power, energy is being recovered
        # a and b are model's constants for recovery to be calibrated
        a, b = 0.1, 0  # Placeholder values
        return -((a * u + b) - CP)

# Define the state-space model function
def state_space_model(y, t, u_func, theta_func):
    s, v, w = y
    u = u_func(t)
    theta = theta_func(s)
    dsdt = f1(v)
    dvdt = f2(u, v, theta)
    dwdt = f3(u, w, u < CP)
    return [dsdt, dvdt, dwdt]

# Placeholder for control strategy function (u(t))
def control_strategy(t):
    # Placeholder for the actual control strategy
    return CP

# Placeholder for road slope as a function of distance (theta(s))
def road_slope(s):
    # Placeholder for the actual road slope function
    return 0

# Initial conditions
s0 = 0  # Initial distance
v0 = 4  # Initial velocity (approximately 15 km/h)
w0 = AWC  # Initial remaining energy

# Time vector
t = np.linspace(0, 3600, 3601)  # Simulate for 1 hour with 1-second intervals

# Solve the state-space model
solution = odeint(state_space_model, [s0, v0, w0], t, args=(control_strategy, road_slope))

# Plotting the results
plt.plot(t, solution[:, 0], label='Distance')
plt.plot(t, solution[:, 1], label='Velocity')
plt.plot(t, solution[:, 2], label='Energy')
plt.legend()
plt.xlabel('Time (seconds)')
plt.ylabel('States')
plt.title('Cyclist State Evolution')
plt.show()
