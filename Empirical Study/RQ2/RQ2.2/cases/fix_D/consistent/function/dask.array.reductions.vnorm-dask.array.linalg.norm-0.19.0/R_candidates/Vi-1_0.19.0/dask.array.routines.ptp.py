@wraps(np.ptp)
def ptp(a, axis=None):
    return a.max(axis=axis) - a.min(axis=axis)
