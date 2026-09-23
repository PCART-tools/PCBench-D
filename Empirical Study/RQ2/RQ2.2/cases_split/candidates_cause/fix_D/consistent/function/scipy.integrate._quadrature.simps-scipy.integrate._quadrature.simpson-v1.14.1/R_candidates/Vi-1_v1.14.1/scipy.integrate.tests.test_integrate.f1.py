def f1(t, x, omega):
    dxdt = [omega*x[1], -omega*x[0]]
    return dxdt
