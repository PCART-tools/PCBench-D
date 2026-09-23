def f2(t, x, omega1, omega2):
    dxdt = [omega1*x[1], -omega2*x[0]]
    return dxdt
