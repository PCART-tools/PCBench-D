def argtopk_aggregate(a_plus_idx, k, axis, keepdims):
    """ Final aggregation function of argtopk

    Invoke argtopk one final time, sort the results internally, drop the data
    and return the index only.
    """
    assert keepdims is True
    a, idx = argtopk(a_plus_idx, k, axis, keepdims)
    axis = axis[0]

    idx2 = np.argsort(a, axis=axis)
    idx = take_along_axis(idx, idx2, axis)
    if k < 0:
        return idx
    return idx[tuple(slice(None, None, -1) if i == axis else slice(None)
                     for i in range(idx.ndim))]
