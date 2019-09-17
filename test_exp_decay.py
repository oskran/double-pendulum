from exp_decay import ExponentialDecay
from matplotlib import pyplot as plt
import numpy as np

# 1a) A class to represent the ODE - Unit test


def test_1a():
    f = ExponentialDecay(0.4)
    assert f(3.2) == -1.28


test_1a()


def test_exp_decay():
    f = ExponentialDecay(0.4)
    assert f(3.2) == -1.28
