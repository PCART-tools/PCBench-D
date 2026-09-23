def reflect(x, axis, depth):
    """ Reflect boundaries of array on the same side

    This is the converse of ``periodic``
    """
    if depth == 1:
        left = ((slice(None, None, None),) * axis +
                (slice(0, 1),) +
                (slice(None, None, None),) * (x.ndim - axis - 1))
    else:
        left = ((slice(None, None, None),) * axis +
                (slice(depth - 1, None, -1),) +
                (slice(None, None, None),) * (x.ndim - axis - 1))
    right = ((slice(None, None, None),) * axis +
             (slice(-1, -depth - 1, -1),) +
             (slice(None, None, None),) * (x.ndim - axis - 1))
    l = x[left]
    r = x[right]

    l, r = _remove_overlap_boundaries(l, r, axis, depth)

    return concatenate([l, x, r], axis=axis)
