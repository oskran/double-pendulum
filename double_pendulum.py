import math
from scipy.integrate import solve_ivp
import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt


class DoublePendulum:
    def __init__(self, L1=1, M1=1, L2=1, M2=1):
        self.L1 = L1
        self.M1 = M1
        self.L2 = L2
        self.M2 = M2
        self.g = 9.81

    def __call__(self, t, y):
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

    def solve(self, y0, T, dt, angles):
        self.dt = dt
        if angles == "deg":
            y0 = [i * (math.pi / 180) for i in y0]

        assert angles in ["deg", "rad"], ValueError

        solved = solve_ivp(self, [0, T], y0, method="Radau", t_eval=np.arange(0, T, dt))

        self.solved = solved

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
        return [self.L1 * math.sin(i) for i in self.theta1]

    @property
    def y1(self):
        return [-self.L1 * math.cos(i) for i in self.theta1]

    @property
    def x2(self):
        return [self.x1[i] + self.L2 * math.sin(j) for i, j in enumerate(self.theta2)]

    @property
    def y2(self):
        return [self.y1[i] - self.L2 * math.cos(j) for i, j in enumerate(self.theta2)]

    @property
    def potential(self):
        P1 = [self.M1 * self.g * (y + self.L1) for y in self.y1]

        P2 = [self.M2 * self.g * (y + self.L1 + self.L2) for y in self.y2]

        P = [P1[i] + P2[i] for i, j in enumerate(P1)]

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
        K1 = [
            (1 / 2) * self.M1 * ((self.vx1[i] ** 2) + (self.vy1[i] ** 2))
            for i, y in enumerate(self.vy1)
        ]

        K2 = [
            (1 / 2) * self.M2 * ((self.vx2[i]) ** 2 + (self.vy2[i] ** 2))
            for i, y in enumerate(self.vy2)
        ]

        return [K1[i] + K2[i] for i, j in enumerate(K1)]

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
            frames=range(len(self.x1)),
            repeat=None,
            interval=1000 * self.dt,
            blit=True,
        )

    def _next_frame(self, i):
        self.pendulums.set_data(
            (0, self.x1[i], self.x2[i]), (0, self.y1[i], self.y2[i])
        )
        return (self.pendulums,)

    def show_animation(self):
        plt.show()

    def save_animation(self):
        self.animation.save("pendulum_motion.mp4", fps=60)
