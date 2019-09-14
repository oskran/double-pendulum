from double_pendulum import DoublePendulum
import math
import numpy as np


L1 = 1
L2 = 1
M2 = 1
M1 = 1
theta1 = math.pi / 6
theta2 = math.pi / 6
omega1 = 0.15
omega2 = 0.15
y0 = (theta1, theta2, omega1, omega2)
T = 10
dt = 0.05

f = DoublePendulum(M1=M1, M2=M2, L1=L1, L2=L2)
f.solve(y0, T, dt, "rad")

f.create_animation()
f.show_animation()
