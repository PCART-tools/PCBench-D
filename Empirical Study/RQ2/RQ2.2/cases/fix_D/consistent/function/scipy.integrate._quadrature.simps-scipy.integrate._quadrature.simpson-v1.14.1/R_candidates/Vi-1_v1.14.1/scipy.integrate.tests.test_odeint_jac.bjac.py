def bjac(y, t):
    n = len(y)
    bjac = np.zeros((4, n), order='F')
    banded5x5.banded5x5_bjac(t, y, 1, 1, bjac)
    return bjac
