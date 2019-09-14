from scipy.integrate import solve_ivp
import numpy as np


class ExponentialDecay:
    def __init__(self, a):
        self.a = a

    def __call__(self, t, u):
        """ Exponential decay function """
        return -self.a * u

    def solve(self, u0, T, dt):
        """ 
        Solves the ODE

        Parameters:
        self.model (function): The ODE to be solved
        u0 (int): The initial value 
        T (int):the end of the time interval
        dt (float):The points where the solution is evaluated

        Returns:
        t (list): Time points
        u (list): Values of the solution at point t
        """
        solved = solve_ivp(
            self, [0, T], [u0], method="Radau", t_eval=np.arange(0, T, dt)
        )

        return solved.t, solved.y
