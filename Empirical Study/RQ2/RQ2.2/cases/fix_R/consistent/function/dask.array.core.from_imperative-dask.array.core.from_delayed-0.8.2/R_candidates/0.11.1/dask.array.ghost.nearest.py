def nearest(x, axis, depth):
    """ Each reflect each boundary value outwards

    This mimics what the skimage.filters.gaussian_filter(... mode="nearest")
    does.
    """
    left = ((slice(None, None, None),) * axis +
            (slice(0, 1),) +
            (slice(None, None, None),) * (x.ndim - axis - 1))
    right = ((slice(None, None, None),) * axis +
             (slice(-1, -2, -1),) +
             (slice(None, None, None),) * (x.ndim - axis - 1))

    l = concatenate([x[left]] * depth, axis=axis)
    r = concatenate([x[right]] * depth, axis=axis)

    l, r = _remove_ghost_boundaries(l, r, axis, depth)

    return concatenate([l, x, r], axis=axis)
