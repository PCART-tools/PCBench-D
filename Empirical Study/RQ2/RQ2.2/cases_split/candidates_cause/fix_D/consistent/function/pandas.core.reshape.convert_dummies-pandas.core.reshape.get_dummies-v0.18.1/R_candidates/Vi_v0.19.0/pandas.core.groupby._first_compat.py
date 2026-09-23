def _first_compat(x, axis=0):
    def _first(x):
        x = np.asarray(x)
        x = x[notnull(x)]
        if len(x) == 0:
            return np.nan
        return x[0]

    if isinstance(x, DataFrame):
        return x.apply(_first, axis=axis)
    else:
        return _first(x)
