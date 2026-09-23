def periodic(x, axis, depth):
    """ Copy a slice of an array around to its other side

    Useful to create periodic boundary conditions for overlap
    """

    left = ((slice(None, None, None),) * axis +
            (slice(0, depth),) +
            (slice(None, None, None),) * (x.ndim - axis - 1))
    right = ((slice(None, None, None),) * axis +
             (slice(-depth, None),) +
             (slice(None, None, None),) * (x.ndim - axis - 1))
    l = x[left]
    r = x[right]

    l, r = _remove_overlap_boundaries(l, r, axis, depth)

    return concatenate([r, x, l], axis=axis)
