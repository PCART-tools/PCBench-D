@np.deprecate(message="scipy.stats.ss is deprecated in scipy 0.17.0")
def ss(a, axis=0):
    return _sum_of_squares(a, axis)
