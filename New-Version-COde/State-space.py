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
    return v

def f2(u, v, theta):
    drag_force = 0.5 * C_d * A * rho * v**2
    rolling_resistance = C_R * g * np.cos(theta)
    gravitational_force = m_b * g * np.sin(theta)
    return (u - (gravitational_force + rolling_resistance + drag_force)) / (m * v)

def f3(u, w):
    if u >= CP:
        return -(u - CP)
    else:
        a, b = 0.1, 0  # Placeholder values
        return -((a * u + b) - CP)

# Placeholder for the Hamiltonian function (assuming it's defined elsewhere)
def hamiltonian(x, u, lambda_):
    L = 1
    f = np.array([f1(x[1]), f2(u, x[1], x[2]), f3(u, x[2])])
    H = L + np.dot(lambda_, f)
    return H

# Simplistic control strategy function
def control_strategy(t, v, w, theta):
    desired_speed_flat = 8.33  # 30 km/h in m/s
    max_speed_uphill = 5.56  # 20 km/h in m/s
    max_speed_downhill = 11.11  # 40 km/h in m/s
    energy_threshold = AWC * 0.1

    if theta > 0:
        if w < energy_threshold or v > max_speed_uphill:
            return CP
        else:
            return CP * 1.2
    elif theta < 0:
        if v > max_speed_downhill:
            return 0
        else:
            return CP * 0.5
    else:
        if w < energy_threshold:
            return CP
        elif v < desired_speed_flat:
            return CP * 1.1
        else:
            return CP

# Define the state-space model function
def state_space_model(y, t, theta_func, lambda_):
    s, v, w, _ = y  # Unpack the current state variables (including Hamiltonian)
    theta = theta_func(s)  # Get the road slope from theta_func
    u = control_strategy(t, v, w, theta)  # Determine control input using the strategy

    if v <= 0 and u > 0:
        # If velocity is zero or negative, we set a minimum positive velocity
        # to prevent division by zero in the dynamics equation
        v = 0.1

    dsdt = f1(v)
    dvdt = f2(u, v, theta)
    dwdt = f3(u, w)
    H = hamiltonian([s, v, w], u, lambda_)

    return [dsdt, dvdt, dwdt, H]


# Placeholder for road slope as a function of distance (theta(s))
def road_slope(s):
    return 0  # Flat road for this example

# Initial conditions
s0 = 0  # Initial distance
v0 = 4  # Start with a non-zero initial velocity (approximately 15 km/h)
w0 = AWC  # Initial remaining energy
H0 = 0   # Initial Hamiltonian, which will be calculated

# Co-state variables (to be determined as part of optimization)
lambda_ = np.array([0.1, 0.1, 0.1])  # Placeholder values

# Time vector for simulation
step_size = 1  # 1 second per step
t = np.arange(0, 3600 + step_size, step_size)  # 3600 seconds with a 1-second interval

# Initial conditions for the state variables and the Hamiltonian
initial_conditions = [s0, v0, w0, H0]

# Solve the state-space model with the Hamiltonian included
augmented_state_solution = odeint(state_space_model, initial_conditions, t, args=(road_slope, lambda_))

# Extract the state variables and Hamiltonian from the solution
s = augmented_state_solution[:, 0]
v = augmented_state_solution[:, 1]
w = augmented_state_solution[:, 2]
H_values = augmented_state_solution[:, 3]

# Plotting the results
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
# plt.plot(t, s, label='Distance (m)')
plt.plot(t, v, label='Velocity (m/s)')
# plt.plot(t, w, label='Energy (J)')
plt.legend()
plt.xlabel('Time (seconds)')
plt.ylabel('States')
plt.title('Cyclist State Evolution')

plt.subplot(2, 1, 2)
plt.plot(t, H_values, label='Hamiltonian', color='purple')
plt.legend()
plt.xlabel('Time (seconds)')
plt.ylabel('Hamiltonian Value')
plt.title('Hamiltonian Evolution Over Time')

plt.tight_layout()
plt.show()
