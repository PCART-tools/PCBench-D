def _last_compat(x, axis=0):
    def _last(x):
        x = np.asarray(x)
        x = x[notnull(x)]
        if len(x) == 0:
            return np.nan
        return x[-1]

    if isinstance(x, DataFrame):
        return x.apply(_last, axis=axis)
    else:
        return _last(x)
