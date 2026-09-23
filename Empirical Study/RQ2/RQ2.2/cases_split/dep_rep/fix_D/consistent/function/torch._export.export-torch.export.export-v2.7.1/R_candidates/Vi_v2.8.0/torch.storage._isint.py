def _isint(x):
    if HAS_NUMPY:
        return isinstance(x, (int, np.integer))
    else:
        return isinstance(x, int)
