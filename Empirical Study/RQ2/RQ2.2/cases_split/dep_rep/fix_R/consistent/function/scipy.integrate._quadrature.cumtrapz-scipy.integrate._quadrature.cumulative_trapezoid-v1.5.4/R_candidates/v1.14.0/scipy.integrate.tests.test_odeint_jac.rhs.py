def rhs(y, t):
    dydt = np.zeros_like(y)
    banded5x5.banded5x5(t, y, dydt)
    return dydt
