import numpy as np
from scipy.integrate import solve_ivp  # For solving differential equations

class Vehicle:
    def __init__(self, params, route):
        """
        Initialize the vehicle with specific parameters.
        params: Dictionary containing vehicle parameters (m, g, mu, rho, Cd, A, eta)
        """
        self.params = params
        self.route = route  # Add this line to store the route as part of the vehicle's state

    
    def state_dynamics(self, t, x, u):
        """
        Computes the derivative of the state vector.
        x: State vector [s, v, W]
        u: Control input (power of the vehicle)
        theta: Road inclination angle
        """
        s, v, W = x 
        theta = self.route.get_incline(s)  # Get the current incline based on the vehicle's position
        m, g, mu, rho, Cd, A, eta = [self.params[k] for k in ('m', 'g', 'mu', 'rho', 'Cd', 'A', 'eta')]
        
        # Force equations
        Fr = 0.5 * rho * Cd * A * v**2
        Ff = mu * m * g
        
        # Dynamics
        dsdt = v
        dvdt = (u / v) - g * (np.sin(theta) + mu * np.cos(theta)) - Fr / m
        
        u_adjusted = min(u, W + self.power_recovery(v) - self.power_consumption(v))
        dWdt = self.power_recovery(v) - self.power_consumption(v) - u_adjusted
        
        return [dsdt, dvdt, dWdt]
    
    def power_recovery(self, v):
        # Assuming linear recovery with velocity
        return self.params['recovery_rate'] * v

    def power_consumption(self, v):
        # Consumption increases quadratically with velocity
        p = self.params
        return (p['mu'] * p['m'] * p['g'] + 0.5 * p['rho'] * p['Cd'] * p['A'] * v**2) * v / (3600 * p['eta'])
