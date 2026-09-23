def _desc_stats(x1, x2, axis=0):
    def _stats(x, axis=0):
        x = np.asarray(x)
        mu = np.mean(x, axis=axis)
        std = np.std(x, axis=axis, ddof=1)
        nobs = x.shape[axis]
        return mu, std, nobs
    return _stats(x1, axis) + _stats(x2, axis)
