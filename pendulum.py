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

    def __call__(self, t=0, y=0):
        """
        The two ODEs to be solves

        Parameters:
        t (float):  Time
        y (n-dimensional vector-valued function): State

        Returns:
        d_theta (float): Derivative of the pendulums position = the velocity
        d_omega (float): Derivative of the velocity / movement = the acceleration
        """

        theta = y[0]
        omega = y[1]

        d_theta = omega

        d_omega = -(self.g / self.L) * np.sin(theta)

        return [d_theta, d_omega]

    # 2b) Solving the equations of motions
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

        solved = solve_ivp(self, [0, T], y0, method="Radau", 
                          t_eval=np.arange(0, T, dt))

        self.solved = solved

    @property
    def t(self):
        if hasattr(self, "solved") == False:
            raise Exception(".solved() has not been called")
        else:
            return self.solved.t

    @property
    def theta(self):
        if hasattr(self, "solved") == False:
            raise Exception(".solved() has not been called")
        else:
            return self.solved.y[0]

    @property
    def omega(self):
        if hasattr(self, "solved") == False:
            raise Exception(".solved() has not been called")
        else:
            return self.solved.y[1]

    # 2d) Translating to Cartesian coordinates
    @property
    def x(self):
        return self.L * np.sin(self.theta)

    @property
    def y(self):
        return -self.L * np.cos(self.theta)

    # 2e) Energy conservation
    @property
    def potential(self):
        return self.M * self.g * (self.y + self.L)

    @property
    def kinetic(self):
        return (1 / 2) * self.M * (self.vx ** 2 + self.vy ** 2)

    @property
    def vx(self):
        return np.gradient(self.x, self.t)

    @property
    def vy(self):
        return np.gradient(self.y, self.t)


# 2g) A Dampened Pendulum


class DampenedPendulum(Pendulum):
    def __init__(self, L=1, M=1, B=0):
        self.B = B  # Dampening paramenter
        self.L = L  # Length of the pendulums rod
        self.M = M  # Mass of the pendulum
        self.g = 9.81

    def __call__(self, t, y):
        """
        Theta gives the pendulums position
        Omega gives the velocity / movement
        """

        theta = y[0]
        omega = y[1]

        d_theta = omega  # Velocity

        damp = (self.B / self.M) * omega

        d_omega = (-(self.g / self.L) * math.sin(theta)) - damp  # Acceleration

        return [d_theta, d_omega]


# 2f) Example use
if __name__ == "__main__":
    L = 2.7
    omega0 = 0.15
    theta0 = 3.14 / 6
    y0 = [theta0, omega0]
    T = 10
    dt = 0.1

    # Create pendulum instance
    f = Pendulum(L=L)

    # Solving
    f.solve(y0, T, dt, "rad")

    # Plotting the motion
    plt.plot(f.t, f.theta)
    plt.show()

    # Plotting the kinetic, potential, and total energy
    plt.plot(f.t, f.potential)  # Potential energy
    plt.plot(f.t, f.kinetic)  # Kinetic energy
    plt.plot(
        f.t, [f.potential[i] + f.kinetic[i] for i, j in enumerate(f.potential)]
    )  # Total energy

    plt.show()

    # 2g) A Dampened Pendulum
    # Plot total energy of the dampened pendulum
    B = 0.5  # Dampening term
    f_dampened = DampenedPendulum(L=L, B=B)
    f_dampened.solve(y0, T, dt, "rad")

    plt.plot(
        f_dampened.t,
        [
            f_dampened.potential[i] + f_dampened.kinetic[i]
            for i, j in enumerate(f_dampened.potential)
        ],
    )

    plt.show()
