def topk_aggregate(a, k, axis, keepdims):
    """ Final aggregation function of topk

    Invoke topk one final time and then sort the results internally.
    """
    assert keepdims is True
    a = topk(a, k, axis, keepdims)
    axis = axis[0]
    a = np.sort(a, axis=axis)
    if k < 0:
        return a
    return a[tuple(slice(None, None, -1) if i == axis else slice(None)
                   for i in range(a.ndim))]
