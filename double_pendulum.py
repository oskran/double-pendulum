import math
from scipy.integrate import solve_ivp
import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt

# 3a) A class for representing the system


class DoublePendulum:
    def __init__(self, L1=1, M1=1, L2=1, M2=1):
        self.L1 = L1
        self.M1 = M1
        self.L2 = L2
        self.M2 = M2
        self.g = 9.81

    def __call__(self, t=0, y=0):
        """Theta gives the pendulums position
        Omega gives the velosity / movement"""

        g = self.g
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

    # 3b) Solving the equations of motions
    def solve(self, y0, T, dt, angles):
        self.dt = dt
        if angles == "deg":
            y0 = [i * (math.pi / 180) for i in y0]

        assert angles in ["deg", "rad"], ValueError

        solved = solve_ivp(self, [0, T], y0, method="Radau", t_eval=np.arange(0, T, dt))

        self.solved = solved

    # 3c) Adding properties
    @property
    def t(self):
        return self.solved.t

    @property
    def theta1(self):
        return self.solved.y[0]

    @property
    def theta2(self):
        return self.solved.y[1]

    @property
    def x1(self):
        return self.L1 * np.sin(self.theta1)

    @property
    def y1(self):
        return -self.L1 * np.cos(self.theta1)

    @property
    def x2(self):
        return self.x1 + self.L2 * np.sin(self.theta2)

    @property
    def y2(self):
        return self.y1 - self.L2 * np.cos(self.theta2)

    # 3d) Checking energy conservation
    @property
    def potential(self):
        P1 = self.M1 * self.g * (self.y1 + self.L1)

        P2 = self.M2 * self.g * (self.y2 + self.L1 + self.L2)

        P = P1 + P2

        return P

    @property
    def vx1(self):
        return np.gradient(self.x1, self.t)

    @property
    def vy1(self):
        return np.gradient(self.y1, self.t)

    @property
    def vx2(self):
        return np.gradient(self.x2, self.t)

    @property
    def vy2(self):
        return np.gradient(self.y2, self.t)

    @property
    def kinetic(self):
        K1 = (1 / 2) * self.M1 * ((self.vx1 ** 2) + (self.vy1 ** 2))

        K2 = (1 / 2) * self.M2 * ((self.vx2) ** 2 + (self.vy2 ** 2))

        return K1 + K2

    # 4a) Setting up the animation
    def create_animation(self):
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

    # 4b) The `_next_frame` method
    def _next_frame(self, i):
        self.pendulums.set_data(
            (0, self.x1[i], self.x2[i]), (0, self.y1[i], self.y2[i])
        )
        return (self.pendulums,)

    # 4c) Interface for animations
    def show_animation(self):
        plt.show()

    def save_animation(self):
        self.animation.save("pendulum_motion.mp4", fps=60)


if __name__ == "__main__":
    # 3d) Checking energy conservation - Plotting
    def plot_energy():
        """ Plots potential, kinetic and total energy """
        theta1 = 90
        theta2 = 90
        omega1 = 0.15
        omega2 = 0.15
        y0 = (theta1, theta2, omega1, omega2)
        T = 10
        dt = 1e-3

        f = DoublePendulum()
        f.solve(y0, T, dt, "deg")

        plt.plot(f.t, f.potential)
        plt.plot(f.t, f.kinetic)
        plt.plot(f.t, f.kinetic + f.potential)

        plt.show()

    # 4d) Creating an animation
    def animate():
        """ Creates, shows, and saves an animation of the pendulum """
        theta1 = 90
        theta2 = 90
        omega1 = 0.15
        omega2 = 0.15
        y0 = (theta1, theta2, omega1, omega2)
        T = 10
        dt = 1e-3

        f = DoublePendulum()
        f.solve(y0, T, dt, "deg")

        f.create_animation()
        f.show_animation()
        f.save_animation()

    plot_energy()
    animate()
