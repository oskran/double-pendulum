from pendulum import Pendulum, DampenedPendulum
import math
import numpy as np
from matplotlib import pyplot as plt
import pytest

# 2a) A class for representing the system


def test_derivatives():
    """ Test that the derivatives are computed correctly """
    f = Pendulum(L=2.7)
    theta = math.pi / 6
    omega = 0.15
    y = [theta, omega]
    excepted = [0.15, -1.816]
    tol = 1e-3
    assert abs(f(y=y)[0] - excepted[0]) < tol
    assert abs(f(y=y)[1] - excepted[1]) < tol


test_derivatives()


def test_rest():
    """ Test that the pendulum stays at rest """
    f = Pendulum()
    theta = 0
    omega = 0
    y = [theta, omega]

    assert f(y=y) == [0, 0]


test_rest()

# 2c) Adding properties for accessing the solutions


def test_2c_not_called():
    """ 
    Test whether an exception is raised if .t, .theta, 
    or .omega are accessed before .solve() is called 
    """
    f = Pendulum()

    with pytest.raises(Exception):
        f.t
        f.omega
        f.theta


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
    assert all(i == 0 for i in f.theta)
    assert all(i == 0 for i in f.omega)


test_2c_called()

# 2d) Translating to Cartesian coordinates - Unit test


def test_r2eql2():
    """ 
    Verifies that the radius squared is almost equal
    to the length of the pendulum rod squared at all times 
    """
    L = 2.7
    omega0 = 0.15
    theta0 = 3.14 / 6
    y0 = [theta0, omega0]
    T = 10
    dt = 0.1
    tol = 1e-3

    f = Pendulum(L=L)
    f.solve(y0, T, dt, "rad")

    r2 = (f.y ** 2) + (f.x ** 2)

    assert abs(r2 - (L ** 2)).all() < tol


test_r2eql2()

if __name__ == '__main__':
    pytest.main()
