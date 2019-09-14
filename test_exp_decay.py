from exp_decay import ExponentialDecay
from matplotlib import pyplot as plt
import numpy as np

a = 0.4
u0 = 1
T = 15
dt = 0.1

decay_model = ExponentialDecay(a)
t, u = decay_model.solve(u0, T, dt)

""" 
def test_1a():
    a = 0.4
    decay_model = ExponentialDecay(a)
    decay_model(u)


test_1a() """


print(t.shape, u.shape)
""" 
def test_1b():
    plt.plot(t, u[0, :])
    plt.show()

test_1b() """
