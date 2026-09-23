@wraps(np.compress)
def compress(condition, a, axis=None):
    if axis is None:
        a = a.ravel()
        axis = 0
    axis = validate_axis(axis, a.ndim)

    # Only coerce non-lazy values to numpy arrays
    if not isinstance(condition, Array):
        condition = np.array(condition, dtype=bool)
    if condition.ndim != 1:
        raise ValueError("Condition must be one dimensional")

    if isinstance(condition, Array):
        if len(condition) < a.shape[axis]:
            a = a[tuple(slice(None, len(condition))
                        if i == axis else slice(None)
                        for i in range(a.ndim))]
        inds = tuple(range(a.ndim))
        out = atop(np.compress, inds, condition, (inds[axis],), a, inds,
                   axis=axis, dtype=a.dtype)
        out._chunks = tuple((np.NaN,) * len(c) if i == axis else c
                            for i, c in enumerate(out.chunks))
        return out
    else:
        # Optimized case when condition is known
        if len(condition) < a.shape[axis]:
            condition = condition.copy()
            condition.resize(a.shape[axis])

        slc = ((slice(None),) * axis + (condition, ) +
               (slice(None),) * (a.ndim - axis - 1))
        return a[slc]
