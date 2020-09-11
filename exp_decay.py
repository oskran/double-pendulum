from scipy.integrate import solve_ivp
import numpy as np
from matplotlib import pyplot as plt


class ExponentialDecay:
    def __init__(self, a):
        self.a = a

    def __call__(self, t=0, u=0):
        """ Exponential decay function """
        return -self.a * u

    def solve(self, u0, T, dt):
        """ Solves the ODE

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
        return solved.t, solved.y[0, :]


if __name__ == "__main__":

    def example_1b():
        a = 0.4
        u0 = 1
        T = 15
        dt = 0.1
        decay_model = ExponentialDecay(a)
        t, u = decay_model.solve(u0, T, dt)

        plt.plot(t, u)
        plt.show()

    example_1b()
