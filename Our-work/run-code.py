import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp  # For solving differential equations
from pmp import discretize_problem
from vehicle import Vehicle  # Assuming vehicle instance is created and available in "vehicle.py"
from route import Route

# Example vehicle parameters
vehicle_params = {
    'm': 18000,  # mass in kg
    'g': 9.8,    # gravity in m/s^2
    'mu': 0.016, # friction coefficient
    'rho': 1.225, # air density in kg/m^3
    'Cd': 0.6,   # drag coefficient
    'A': 8.16,   # frontal area in m^2
    'eta': 0.86,  # efficiency
    'recovery_rate': 100 # recovery rate
}

# Define a route with uphills and downhills
route_segments = [
    (1000, 0),       # Flat for 1 km
    (500, np.pi/18), # Uphill with 10 degrees incline for 500 m
    (1000, 0),       # Flat for 1 km
    (500, -np.pi/18) # Downhill with 10 degrees decline for 500 m
]
route = Route(route_segments)

# Update vehicle initialization to pass the route
vehicle = Vehicle(vehicle_params, route)

initial_state = [0, 5, 10000]  # [s0 (m), v0 (m/s), W0 (Joules)], with some initial energy for demonstration
time_horizon = 300  # Extended time to cover the entire route
dt = 1  # Time step for discretization in seconds

times, states = discretize_problem(vehicle, initial_state, time_horizon, dt)

# Plotting the results
plt.figure(figsize=(12, 8))

# Distance over time
plt.subplot(311)
plt.plot(times, states[:, 0], label='Distance')
plt.xlabel('Time (s)')
plt.ylabel('Distance (m)')
plt.legend()

# Velocity over time
plt.subplot(312)
plt.plot(times, states[:, 1], label='Velocity')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.legend()

# Energy over time
plt.subplot(313)
plt.plot(times, states[:, 2], label='Energy')
plt.xlabel('Time (s)')
plt.ylabel('Energy (Joules)')
plt.legend()

plt.tight_layout()
plt.show()