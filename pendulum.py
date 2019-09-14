import math
from scipy.integrate import solve_ivp
import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt


class Pendulum:
    def __init__(self, L=1, M=1):
        self.L = L  # Length of the pendulums rod
        self.M = M  # Mass of the pendulum
        self.g = 9.81

    def __call__(self, t, y):
        """


        Parameters:

        Returns:
        d_theta (): Derivative of the pendulums position = the velocity
        d_omega (): Derivative of the velocity / movement = the acceleration
        """

        theta = y[0]
        omega = y[1]

        d_theta = omega  # Velocity

        d_omega = -(self.g / self.L) * math.sin(theta)  # Acceleration

        return [d_theta, d_omega]

    def solve(self, y0, T, dt, angles):
        """ 
        Solves the ODE

        Parameters:
        self.model (function): The ODE to be solved
        u0 (int): The initial value 
        T (int): The end of the time interval
        dt (float): The points where the solution is evaluated
        angles (string): Whether the initial condition is gives as degrees or radius
        """

        if angles == "deg":
            [y0[i] * (math.pi / 180) for i in y0]

        assert angles in ["deg", "rad"], ValueError

        solved = solve_ivp(self, [0, T], y0, method="Radau", t_eval=np.arange(0, T, dt))

        self.solved = solved

    @property
    def t(self):
        return self.solved.t

    @property
    def theta(self):
        return self.solved.y[0]

    @property
    def omega(self):
        return self.solved.y[1]

    @property
    def x(self):
        return [self.L * math.sin(i) for i in self.theta]

    @property
    def y(self):
        return [-self.L * math.cos(i) for i in self.theta]

    @property
    def potential(self):
        # Potential energy
        P = [self.M * self.g * (y + self.L) for y in self.y]
        return P

    @property
    def kinetic(self):
        K = [
            (1 / 2) * self.M * (self.vx[i] ** 2 + self.vy[i] ** 2)
            for i, y in enumerate(self.vy)
        ]

        return K

    @property
    def vx(self):
        return np.gradient(self.x, self.t)

    @property
    def vy(self):
        return np.gradient(self.y, self.t)


class DampenedPendulum(Pendulum):
    def __init__(self, L=1, M=1, B=0):
        self.B = B  # Dampening paramenter
        self.L = L  # Length of the pendulums rod
        self.M = M  # Mass of the pendulum
        self.g = 9.81

    def __call__(self, t, y):
        """Theta gives the pendulums position
        Omega gives the velosity / movement"""

        theta = y[0]
        omega = y[1]

        d_theta = omega  # Velocity

        damp = (self.B / self.M) * omega

        d_omega = (-(self.g / self.L) * math.sin(theta)) - damp  # Acceleration

        return [d_theta, d_omega]
