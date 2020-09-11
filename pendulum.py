import math
from scipy.integrate import solve_ivp
import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt


class Pendulum:
    """
    A Pendulum object
    
    Parameters
    ----------
    L: float
        The length of the pendulum rod in meters.
    M: float
        The mass of the pendulum in kg.
    g: float
        The gravitational force in (m/s)^2
    """

    def __init__(self, L=1, M=1):
        self.L = L
        self.M = M
        self.G = 9.81

    def __call__(self, t=0, y=0):
        """
        The two ODEs to be solves

        Takes a time and a state parameter and returns the derivative of the
        position and the velocity.

        Parameters
        ----------
        t: float
            Time
        y: array_like
            State

        Returns
        -------
        d_theta: ndarray
            Derivative of the pendulums position = the velocity
        d_omega: ndarray
            Derivative of the velocity / movement = the acceleration
        """

        theta = y[0]
        omega = y[1]

        d_theta = np.array(omega)

        d_omega = -(self.G / self.L) * np.sin(theta)

        return [d_theta, d_omega]

    def solve(self, y0, T, dt, angles):
        """ 
        Solves the ODE given an initial value

        Parameters
        ----------
        self.model: function
            The ODE to be solved
        u0: array like, shape (n,)
            Initial value
        T: int 
            The end of the time interval
        dt: float
            Time between the points where the solution is evaluated
        angles: string
            Whether the initial condition is gives as degrees or radius
        """

        if angles == "deg":
            y0[0] * math.pi

        assert angles in ["deg", "rad"], ValueError

        solved = solve_ivp(self, [0, T], y0, method="Radau", t_eval=np.arange(0, T, dt))

        self.solved = solved

    @property
    def t(self):
        """ Returns the time points where the solution was evaluated """
        if hasattr(self, "solved") == False:
            raise Exception(".solved() has not been called")
        else:
            return self.solved.t

    @property
    def theta(self):
        """ Returns the pendulums position, where it was evaluated """
        if hasattr(self, "solved") == False:
            raise Exception(".solved() has not been called")
        else:
            return self.solved.y[0]

    @property
    def omega(self):
        """ Returns the pendulums velocity, where it was evaluated """
        if hasattr(self, "solved") == False:
            raise Exception(".solved() has not been called")
        else:
            return self.solved.y[1]

    @property
    def x(self):
        """ Converts the horizontal position from polar to cartesian coordinates  """
        return self.L * np.sin(self.theta)

    @property
    def y(self):
        """ Converts the vertical position from polar to cartesian coordinates  """
        return -self.L * np.cos(self.theta)

    @property
    def potential(self):
        """ Calculates potensial energy """
        return self.M * self.G * (self.y + self.L)

    @property
    def kinetic(self):
        """ Calculates kinetic energy """
        return (1 / 2) * self.M * (self.vx ** 2 + self.vy ** 2)

    @property
    def vx(self):
        """ Calculates the velocity of the pendulum """
        return np.gradient(self.x, self.t)

    @property
    def vy(self):
        """ Calculates the velocity of the pendulum """
        return np.gradient(self.y, self.t)


class DampenedPendulum(Pendulum):
    """
    A Pendulum object
    
    Parameters
    ----------
    B: float
        The dampening parameter.
    L: float
        The length of the pendulum rod in meters.
    M: float
        The mass of the pendulum in kg.
    g: float
        The gravitational force in (m/s)^2.
    """

    def __init__(self, L=1, M=1, B=0):
        self.B = B
        self.L = L
        self.M = M
        self.G = 9.81

    def __call__(self, t, y):
        theta = y[0]
        omega = y[1]

        d_theta = omega  # Velocity

        damp = (self.B / self.M) * omega

        d_omega = (-(self.G / self.L) * math.sin(theta)) - damp

        return [d_theta, d_omega]


if __name__ == "__main__":

    def plot_motion():
        """ Plots the motion of the pendulum """
        omega0 = 0.15
        theta0 = 90
        y0 = [theta0, omega0]
        T = 10
        dt = 1e-3

        f = Pendulum()
        f.solve(y0, T, dt, "deg")

        plt.plot(f.t, f.theta)
        plt.show()

    def plot_energy():
        """ Plots the potential, kinetic, and total energy of the pendulum """
        omega0 = 0.15
        theta0 = 90
        y0 = [theta0, omega0]
        T = 10
        dt = 1e-3

        f = Pendulum()
        f.solve(y0, T, dt, "deg")

        plt.plot(f.t, f.potential)
        plt.plot(f.t, f.kinetic)
        plt.plot(f.t, f.potential + f.kinetic)

        plt.show()

    def plot_dampened_energy():
        """ Plots the total energy of the dampened pendulum  """
        omega0 = 0.15
        theta0 = 90
        y0 = [theta0, omega0]
        T = 10
        dt = 1e-3
        B = 0.5  # Dampening term

        f_dampened = DampenedPendulum(B=B)
        f_dampened.solve(y0, T, dt, "rad")

        plt.plot(f_dampened.t, f_dampened.potential + f_dampened.kinetic)

        plt.show()

    plot_motion()
    plot_energy()
    plot_dampened_energy()
