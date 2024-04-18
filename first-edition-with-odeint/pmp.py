import numpy as np
from scipy.integrate import solve_ivp  # For solving differential equations
from vehicle import Vehicle

# Updated function in pmp.py without theta parameter
def discretize_problem(vehicle, initial_state, time_horizon, dt=0.1):
    """
    Integrates the vehicle's state over the given time horizon, considering the route's incline.
    """
    times = np.arange(0, time_horizon + dt, dt)  # Include the end point for plotting

    # Adjust vehicle dynamics function to remove theta as a parameter
    def vehicle_dynamics(t, x):
        u = optimal_control(x)  # Assuming optimal_control can operate on the state vector x
        return vehicle.state_dynamics(t, x, u)

    # Solve the initial value problem
    sol = solve_ivp(vehicle_dynamics, [0, time_horizon], initial_state, t_eval=times, method='RK45')
    
    return sol.t, sol.y.T

# Within discretize_problem in pmp.py

def vehicle_dynamics(t, x):
    if x[0] >= vehicle.route.total_distance:  # If the vehicle has reached the end of the route
        return [0, 0, 0]  # Stop updating the state
    u = optimal_control(x)
    return vehicle.state_dynamics(t, x, u)


def optimal_control(state):
    _, v, W = state  # Current state: velocity and energy
    
    return min(200, W * 0.01)  # Example dynamic control based on energy


def hamiltonian(state, co_state, u, theta):
    """
    Calculates the Hamiltonian given the current state, co-state, control input (u), and theta.

    state: Current state vector [s, v, W]
    co_state: Vector of co-state variables (Lagrange multipliers)
    u: Control input (power of the vehicle)
    theta: Road inclination angle
    """
    # For demonstration, let's just focus on the kinetic part of the Hamiltonian
    _, v, _ = state
    _, lambda_v, lambda_W = co_state
    H = lambda_v * (u / (v if v != 0 else 1e-5)) - lambda_W * u  # Simplified Hamiltonian
    return H


