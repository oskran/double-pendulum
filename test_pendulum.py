from pendulum import Pendulum, DampenedPendulum
import math
import numpy as np
from matplotlib import pyplot as plt

# a)
""" def test_2a():
    omega = 0
    theta = 0
    y = [theta, omega]

    f = Pendulum()
    f() """


# b)

# c)
def test_2c_not_called():
    """ Test whether an exception is raised if .t, .theta, or .omega are accessed before .solve() is called """

    f = Pendulum()
    try:
        f.t
        f.theta
        f.omega
    except:
        return print(".solve() has not been called")


test_2c_not_called()


def test_2c_called():
    """ 
    Checks that t_i ==  i*dt, and that the .theta and .omega
    arrays are full of zeros when the initial condition is [0, 0]
     """

    f = Pendulum()
    omega0 = 0
    theta0 = 0
    T = 10
    dt = 0.1
    y0 = [theta0, omega0]
    f.solve(y0, T, dt, "rad")
    assert (f.t == np.arange(0, T, dt)).all()
    assert (f.theta == [0] * len(f.theta)).all()
    assert (f.omega == [0] * len(f.omega)).all()


test_2c_called()

# d)
def test_r2eql2():
    """ Vertifies that the radius squared is almost equal
    to the lenght of the pendulum rod squared at all times """
    L = 2.7
    omega0 = 0.15
    theta0 = 3.14 / 6
    y0 = [theta0, omega0]
    T = 10
    dt = 0.1

    f = Pendulum(L=L)
    f.solve(y0, T, dt, "rad")

    r2 = [(f.y[i] ** 2) + (f.x[i] ** 2) for i, j in enumerate(f.y)]

    assert [i - (L ** 2) < abs(0.001) for i in r2]


test_r2eql2()

# e)
# Example use:
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

# f)
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
