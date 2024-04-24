import numpy as np
import matplotlib.pyplot as plt
from vehicle import Vehicle
from route import Route
from simulation import Simulation

# Initialize the Vehicle with appropriate parameters
vehi = Vehicle(mass=18000,
               frontal_area=8.16,
               velocity_init=20,
               energy_left=300,
               velocity_max=120,
               energy_max=300)

# Define the Route. Ensure the parameters for each segment are correct (distance, incline angle, and friction coefficient)
rout = Route(((50, 0, 0.015),  # Each tuple represents a segment: (distance in meters, incline angle in degrees, friction coefficient)
              (20, 10, 0.015),
              (50, -10, 0.015)))

sim = Simulation(vehi, rout, distance_step=10)  # Optionally, you can specify other parameters like drag_coefficient or efficiency

sim.simulate()

sim.plot_results()
