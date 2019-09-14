from pendulum import Pendulum
import math
import numpy as np

L = 2.7
omega = 0.15
theta = math.pi / 6
t = np.linspace(1, 10, 100)
y = (theta, omega)
dt = 1
T = 10

# a)


# b)
omega0 = 0
theta0 = 0
y0 = [theta0, omega0]


f = Pendulum(L)
f.solve(y0, T, dt, "rad")
print(f.theta, f.omega)


# d)
def test_r2eql2():
    r2 = [(f.y[i] ** 2) + (f.x[i] ** 2) for i, j in enumerate(f.y)]
    assert r2 == [L ** 2] * len(r2)


test_r2eql2()

# f)


f.create_animation()
f.show_animation()
