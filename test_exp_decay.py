from exp_decay import ExponentialDecay
import pytest


# 1a) A class to represent the ODE - Unit test
def test_1a():
    """ 
    Tests that the calculated derivative
     of u is right gives some parameter values 
    """
    tol = 1e-15
    expected = -1.28
    f = ExponentialDecay(a=0.4)

    calc = abs(f(u=3.2) - expected)
    msg = "Obs: The derivative is not equal to its expected value"
    assert calc < tol, msg


# if __name__ == "__main__":
#     test_1a()

if __name__ == '__main__':
    pytest.main()
