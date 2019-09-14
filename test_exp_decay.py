from exp_decay import ExponentialDecay
from matplotlib import pyplot as plt

a = 0.4

u0 = 1

T = 30

dt = list(range(0, 10, 1))

decay_model = ExponentialDecay(a)

t, u = decay_model.solve(u0, T, dt)


print(t)

print()

print(u)

""" plt.plot(t, u)
plt.show()
 """
