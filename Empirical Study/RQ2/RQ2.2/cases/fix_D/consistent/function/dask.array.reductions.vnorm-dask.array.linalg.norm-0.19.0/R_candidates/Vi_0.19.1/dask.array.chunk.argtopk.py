def argtopk(a_plus_idx, k, axis, keepdims):
    """ Chunk and combine function of argtopk

    Extract the indices of the k largest elements from a on the given axis.
    If k is negative, extract the indices of the -k smallest elements instead.
    Note that, unlike in the parent function, the returned elements
    are not sorted internally.
    """
    assert keepdims is True
    axis = axis[0]

    if isinstance(a_plus_idx, list):
        a_plus_idx = list(flatten(a_plus_idx))
        a = np.concatenate([ai for ai, _ in a_plus_idx], axis)
        idx = np.concatenate([broadcast_to(idxi, ai.shape)
                              for ai, idxi in a_plus_idx], axis)
    else:
        a, idx = a_plus_idx

    if abs(k) >= a.shape[axis]:
        return a_plus_idx

    idx2 = np.argpartition(a, -k, axis=axis)
    k_slice = slice(-k, None) if k > 0 else slice(-k)
    idx2 = idx2[tuple(k_slice if i == axis else slice(None)
                      for i in range(a.ndim))]
    return take_along_axis(a, idx2, axis), take_along_axis(idx, idx2, axis)
