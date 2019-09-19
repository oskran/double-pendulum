from double_pendulum import DoublePendulum
from matplotlib import pyplot as plt
import numpy as np
import pytest


def test_derivatives():
    """ Test that the derivatives are computed correctly """

    f = DoublePendulum()
    theta1 = 90
    theta2 = 90
    omega1 = 0.15
    omega2 = 0.15
    y = (theta1, theta2, omega1, omega2)

    excepted = [0.15, 0.15, -8.770, 0]
    tol = 1e-3

    for i, ex in enumerate(excepted):
        assert abs(f(y=y)[i] - ex) < tol


test_derivatives()


def test_rest():
    """ Tests that the pendulum stays in place if both joints start at rest """
    theta1 = 0
    theta2 = 0
    omega1 = 0
    omega2 = 0
    y0 = (theta1, theta2, omega1, omega2)
    T = 10
    dt = 1e-3

    f = DoublePendulum()
    f.solve(y0, T, dt, "deg")

    assert all(i == 0 for i in f.theta1)
    assert all(i == 0 for i in f.theta2)


test_rest()


def test_stable_energy():
    """ 
    Tests that the largest deviation from mean
    total energy is smaller than some value 
    """
    theta1 = 90
    theta2 = 90
    omega1 = 0.15
    omega2 = 0.15
    y0 = (theta1, theta2, omega1, omega2)
    T = 10
    dt = 1e-3
    tol = 0.1
    f = DoublePendulum()
    f.solve(y0, T, dt, "deg")

    total = f.potential + f.kinetic

    assert (abs(max(total) - np.mean(total))) < tol
    assert (abs(min(total) - np.mean(total))) < tol


test_stable_energy()

if __name__ == '__main__':
    pytest.main()
