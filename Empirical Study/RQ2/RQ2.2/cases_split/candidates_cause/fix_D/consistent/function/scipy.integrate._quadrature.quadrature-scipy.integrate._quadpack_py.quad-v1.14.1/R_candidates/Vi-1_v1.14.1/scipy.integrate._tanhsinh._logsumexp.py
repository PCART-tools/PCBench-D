def _logsumexp(x, axis=0):
    # logsumexp raises with empty array
    x = np.asarray(x)
    shape = list(x.shape)
    if shape[axis] == 0:
        shape.pop(axis)
        return np.full(shape, fill_value=-np.inf, dtype=x.dtype)
    else:
        return special.logsumexp(x, axis=axis)
