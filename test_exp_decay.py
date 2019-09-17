from exp_decay import ExponentialDecay
from matplotlib import pyplot as plt
import numpy as np

a = 0.4
u0 = 1
T = 15
dt = 0.1

decay_model = ExponentialDecay(a)
t, u = decay_model.solve(u0, T, dt)

# Not working
""" def test_1a():
    a = 0.4
    decay_model = ExponentialDecay(a)
    assert decay_model(u) == −1.28


test_1a() """

