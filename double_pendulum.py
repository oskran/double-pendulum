import math
from scipy.integrate import solve_ivp
import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt


class DoublePendulum:
    """
    A double Pendulum object
    
    Parameters
    ----------
    L1: float
        The length of the first pendulum rod in meters.
    M1: float
        The mass of the first pendulum in kg.
    L2: float
        The length of the second pendulum rod in meters.
    M2: float
        The mass of the second pendulum in kg.    
    g: float
        The gravitational force in (m/s)^2
    """

    def __init__(self, L1=1, M1=1, L2=1, M2=1):
        self.L1 = L1
        self.M1 = M1
        self.L2 = L2
        self.M2 = M2
        self.G = 9.81

    def __call__(self, t=0, y=0):
        """
        The ODEs to be solved

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
        d_theta1: ndarray
            Derivative of the first pendulums position = the velocity
        d_theta2: ndarray
            Derivative of the second pendulums position = the velocity            
        d_omega1: ndarray
            Derivative of the first pendulums velocity = the acceleration
        d_omega2: ndarray
            Derivative of the second pendulums velocity = the acceleration
        """

        g = self.G
        L1 = self.L1
        M1 = self.M1
        L2 = self.L2
        M2 = self.M2
        theta1 = y[0]
        theta2 = y[1]
        omega1 = y[2]
        omega2 = y[3]
        delta_theta = theta2 - theta1

        d_theta1 = omega1
        d_theta2 = omega2

        d_omega1 = (
            (M2 * L1 * (omega1 ** 2) * math.sin(delta_theta) * math.cos(delta_theta))
            + (M2 * g * math.sin(theta2) * math.cos(delta_theta))
            + (M2 * L2 * (omega2 ** 2) * math.sin(delta_theta))
            - ((M1 + M2) * g * math.sin(theta1))
        ) / (((M1 + M2) * L1) - (M2 * L1 * (math.cos(delta_theta) ** 2)))

        d_omega2 = (
            (-M2 * L2 * (omega2 ** 2) * math.sin(delta_theta) * math.cos(delta_theta))
            + ((M1 + M2) * g * math.sin(theta1) * math.cos(delta_theta))
            - ((M1 + M2) * L1 * (omega1 ** 2) * math.sin(delta_theta))
            - ((M1 + M2) * g * math.sin(theta2))
        ) / (((M1 + M2) * L2) - (M2 * L2 * (math.cos(delta_theta) ** 2)))

        return [d_theta1, d_theta2, d_omega1, d_omega2]

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
        self.dt = dt
        if angles == "deg":
            y0[0] = y0[0] * (math.pi / 180)
            y0[1] = y0[1] * (math.pi / 180)

        assert angles in ["deg", "rad"], ValueError

        solved = solve_ivp(self, [0, T], y0, method="Radau", t_eval=np.arange(0, T, dt))

        self._solved = solved

    @property
    def t(self):
        """ Returns the time points where the solution was evaluated """
        return self._solved.t

    @property
    def theta1(self):
        """ Returns the first pendulums position, where it was evaluated """
        if hasattr(self, "solved") == False:
            raise Exception(".solved() has not been called")
        else:
            return self._solved.y[0]

    @property
    def theta2(self):
        """ Returns the second pendulums position, where it was evaluated """
        if hasattr(self, "solved") == False:
            raise Exception(".solved() has not been called")
        else:
            return self._solved.y[1]

    @property
    def x1(self):
        """ 
        Converts the horizontal position of the first pendulum from polar
        to cartesian coordinates  
        """
        return self.L1 * np.sin(self.theta1)

    @property
    def y1(self):
        """ 
        Converts the vertical position of the first pendulum from polar 
        to cartesian coordinates  
        """
        return -self.L1 * np.cos(self.theta1)

    @property
    def x2(self):
        """ 
        Converts the horizontal position of the second pendulum from 
        polar to cartesian coordinates  
        """
        return self.x1 + self.L2 * np.sin(self.theta2)

    @property
    def y2(self):
        """ 
        Converts the vertical position of the second pendulum from polar 
        to cartesian coordinates  
        """
        return self.y1 - self.L2 * np.cos(self.theta2)

    @property
    def potential(self):
        """ Calculates potensial energy """
        P1 = self.M1 * self.G * (self.y1 + self.L1)

        P2 = self.M2 * self.G * (self.y2 + self.L1 + self.L2)

        P = P1 + P2

        return P

    @property
    def vx1(self):
        """ Calculates the velocity of the first pendulum """
        return np.gradient(self.x1, self.t)

    @property
    def vy1(self):
        """ Calculates the velocity of the first pendulum """
        return np.gradient(self.y1, self.t)

    @property
    def vx2(self):
        """ Calculates the velocity of the second pendulum """
        return np.gradient(self.x2, self.t)

    @property
    def vy2(self):
        """ Calculates the velocity of the second pendulum """
        return np.gradient(self.y2, self.t)

    @property
    def kinetic(self):
        """ Calculates kintetic energy """
        K1 = (1 / 2) * self.M1 * ((self.vx1 ** 2) + (self.vy1 ** 2))

        K2 = (1 / 2) * self.M2 * ((self.vx2) ** 2 + (self.vy2 ** 2))

        return K1 + K2

    def create_animation(self):
        """ Creates an animation of the pendulum """
        # Create empty figure
        fig = plt.figure()

        # Configure figure
        plt.axis("equal")
        plt.axis("off")
        plt.axis((-3, 3, -3, 3))

        # Make an "empty" plot object to be updated throughout the animation
        self.pendulums, = plt.plot([], [], "o-", lw=2)

        # Call FuncAnimation
        self.animation = animation.FuncAnimation(
            fig,
            self._next_frame,
            frames=range(0, len(self.x1), 16),
            repeat=None,
            interval=1,
            blit=True,
        )

    def _next_frame(self, i):
        """ Creates a frame in the animation """
        self.pendulums.set_data(
            (0, self.x1[i], self.x2[i]), (0, self.y1[i], self.y2[i])
        )
        return (self.pendulums,)

    def show_animation(self):
        """ Displays the animation """
        plt.show()

    def save_animation(self):
        """ Saves the animation """
        self.animation.save("example_simulation.mp4", fps=60)


if __name__ == "__main__":

    def plot_energy():
        """ Plots potential, kinetic and total energy """
        theta1 = 90
        theta2 = 90
        omega1 = 0.15
        omega2 = 0.15
        y0 = [theta1, theta2, omega1, omega2]
        T = 10
        dt = 1e-3

        f = DoublePendulum()
        f.solve(y0, T, dt, "deg")

        plt.plot(f.t, f.potential)
        plt.plot(f.t, f.kinetic)
        plt.plot(f.t, f.kinetic + f.potential)

        plt.show()

    def animate():
        """ Creates, shows, and saves an animation of the pendulum """
        theta1 = 90
        theta2 = 90
        omega1 = 0.15
        omega2 = 0.15
        y0 = [theta1, theta2, omega1, omega2]
        T = 10
        dt = 1e-3

        f = DoublePendulum()
        f.solve(y0, T, dt, "deg")

        f.create_animation()
        f.show_animation()
        f.save_animation()

    plot_energy()
    animate()
