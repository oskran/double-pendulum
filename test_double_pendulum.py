from double_pendulum import DoublePendulum
import math
import numpy as np
from matplotlib import pyplot as plt

# Parameters:
L1 = 1
L2 = 1
M2 = 1
M1 = 1
theta1 = 90
theta2 = 90
omega1 = 0.15
omega2 = 0.15
y0 = (theta1, theta2, omega1, omega2)
T = 10
dt = 0.1

# Create object and solve:
f = DoublePendulum(M1=M1, M2=M2, L1=L1, L2=L2)
f.solve(y0, T, dt, "deg")

# c)
# Plots potetial, kinetic and total energy
""" plt.plot(f.t, f.potential)  # Potential energy
plt.plot(f.t, f.kinetic)  # Kinetic energy
plt.plot(
    f.t, [f.potential[i] + f.kinetic[i] for i, j in enumerate(f.potential)]
)  # Total energy

plt.show() """

# Create animation and save it
f.create_animation()
f.show_animation()
f.save_animation()
