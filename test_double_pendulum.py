from double_pendulum import DoublePendulum
from matplotlib import pyplot as plt
import numpy as np


def test_stable_energy():
    """ Tests that the largest deviation from mean
    total energy is smaller than some value """
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
