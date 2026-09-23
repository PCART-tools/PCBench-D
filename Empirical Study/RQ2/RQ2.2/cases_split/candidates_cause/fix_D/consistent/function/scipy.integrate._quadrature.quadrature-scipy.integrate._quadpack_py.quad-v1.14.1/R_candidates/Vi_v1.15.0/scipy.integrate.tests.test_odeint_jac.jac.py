def jac(y, t):
    n = len(y)
    jac = np.zeros((n, n), order='F')
    banded5x5.banded5x5_jac(t, y, 1, 1, jac)
    return jac
