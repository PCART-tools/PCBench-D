def topk(a, k, axis, keepdims):
    """ Chunk and combine function of topk

    Extract the k largest elements from a on the given axis.
    If k is negative, extract the -k smallest elements instead.
    Note that, unlike in the parent function, the returned elements
    are not sorted internally.
    """
    assert keepdims is True
    axis = axis[0]
    if abs(k) >= a.shape[axis]:
        return a

    a = np.partition(a, -k, axis=axis)
    k_slice = slice(-k, None) if k > 0 else slice(-k)
    return a[tuple(k_slice if i == axis else slice(None)
                   for i in range(a.ndim))]
