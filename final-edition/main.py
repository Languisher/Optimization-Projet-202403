import numpy as np
import matplotlib.pyplot as plt

from vehicle import Vehicle
from route import Route
from simulation import Simulation

# Assuming you have defined velocity_max and energy_max in your Vehicle class
velocity_max = 30  # maximum velocity in m/s, example value
energy_max = 1000000  # maximum energy in Joules, example value

# Initialize the Vehicle with a starting velocity and total energy
vehi = Vehicle(velocity=10, energy_left=1000, velocity_max=velocity_max, energy_max=energy_max)

# Define the Route with tuples of (distance, inclination)
# For example, 3 segments with different distances and inclinations
rout = Route(((200, 0.5), (300, -1), (400, 1.5)))

# Initialize the Simulation with the vehicle and the route
sim = Simulation(vehi, rout)

# Run the simulation
sim.simulate()

# Plot the results
sim.plot_results()

print()