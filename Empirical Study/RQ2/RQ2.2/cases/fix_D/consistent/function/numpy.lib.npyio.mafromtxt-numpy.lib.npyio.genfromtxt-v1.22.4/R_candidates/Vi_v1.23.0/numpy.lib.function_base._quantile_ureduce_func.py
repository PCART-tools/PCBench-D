def _quantile_ureduce_func(
        a: np.array,
        q: np.array,
        axis: int = None,
        out=None,
        overwrite_input: bool = False,
        method="linear",
) -> np.array:
    if q.ndim > 2:
        # The code below works fine for nd, but it might not have useful
        # semantics. For now, keep the supported dimensions the same as it was
        # before.
        raise ValueError("q must be a scalar or 1d")
    if overwrite_input:
        if axis is None:
            axis = 0
            arr = a.ravel()
        else:
            arr = a
    else:
        if axis is None:
            axis = 0
            arr = a.flatten()
        else:
            arr = a.copy()
    result = _quantile(arr,
                       quantiles=q,
                       axis=axis,
                       method=method,
                       out=out)
    return result
