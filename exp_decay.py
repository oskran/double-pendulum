from scipy.integrate import solve_ivp


class ExponentialDecay:
    def __init__(self, a):
        self.a = a

    def model(self, t, u):
        return -self.a * u

    def solve(self, u0, T, dt):
        solved = solve_ivp(self.model, [0, T], [u0], method="Radau", t_eval=dt)

        return solved.t, solved.y

    def __call__(self):
        return self.model
