import numpy as np
import matplotlib.pyplot as plt

from route import Route
from vehicle import Vehicle
from dynamics import *
from pmp import *

# Example vehicle parameters
vehicle_params = {
    'm': 18000,  # mass in kg
    'g': 9.8,    # gravity in m/s^2
    'mu': 0.016, # friction coefficient
    'rho': 1.225, # air density in kg/m^3
    'Cd': 0.6,   # drag coefficient
    'A': 8.16,   # frontal area in m^2
    'eta': 0.86,  # efficiency
    'recovery_rate': 0.8 # recovery rate
}

# Define a route with uphills and downhills
route_segments = [
    (1000, 0),       # Flat for 1 km
    (500, np.pi/5), # Uphill with 36 degrees incline for 500 m
    (1000, 0),       # Flat for 1 km
    (500, -np.pi/5) # Downhill with 36 degrees decline for 500 m
]


# ------------------------------ Initialize the circumstance --------------------------

route = Route(route_segments)
vehicle = Vehicle(vehicle_params, route)


initial_state = [0, 5, 10000]  # [s0 (m), v0 (m/s), W0 (Joules)], with some initial energy for demonstration
time_horizon = 300  # Extended time to cover the entire route
dt = 1  # Time step for discretization in seconds

times, states = discretize_problem(vehicle, initial_state, time_horizon, dt)

# Adjusted plotting commands in run-code.py

plt.figure(figsize=(12, 9))

# Distance over time x(t)
plt.subplot(311)
plt.plot(times, states[:, 0], 'b-', label='Distance over Time')
plt.xlim([0, times[-1]])
plt.ylim([0, route.total_distance])
plt.xlabel('Time (s)')
plt.ylabel('Distance (m)')
plt.legend()

# Velocity as a function of distance v(x)
plt.subplot(312)
plt.plot(states[:, 0], states[:, 1], 'r-', label='Velocity as a Function of Distance')
plt.xlim([0, route.total_distance])
plt.xlabel('Distance (m)')
plt.ylabel('Velocity (m/s)')
plt.legend()

# Energy as a function of distance E(x)
plt.subplot(313)
plt.plot(states[:, 0], states[:, 2], 'g-', label='Energy as a Function of Distance')
plt.xlim([0, route.total_distance])
plt.xlabel('Distance (m)')
plt.ylabel('Energy (Joules)')
plt.legend()

plt.tight_layout()
plt.show()
