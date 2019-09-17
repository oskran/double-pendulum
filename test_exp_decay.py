from exp_decay import ExponentialDecay
from matplotlib import pyplot as plt
import numpy as np

# 1a)


def test_exp_decay():
    f = ExponentialDecay(0.4)
    assert f(3.2) == -1.28
