def _zsqrt(x):
    with np.errstate(all='ignore'):
        result = np.sqrt(x)
        mask = x < 0

    from pandas import DataFrame
    if isinstance(x, DataFrame):
        if mask.values.any():
            result[mask] = 0
    else:
        if mask.any():
            result[mask] = 0

    return result
