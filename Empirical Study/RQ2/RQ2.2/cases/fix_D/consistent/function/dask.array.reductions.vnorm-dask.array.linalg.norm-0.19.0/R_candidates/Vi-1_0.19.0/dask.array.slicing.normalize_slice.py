def normalize_slice(idx, dim):
    """ Normalize slices to canonical form

    Parameters
    ----------
    idx: slice or other index
    dim: dimension length

    Examples
    --------
    >>> normalize_slice(slice(0, 10, 1), 10)
    slice(None, None, None)
    """

    if isinstance(idx, slice):
        if math.isnan(dim):
            return idx
        start, stop, step = idx.indices(dim)
        if step > 0:
            if start == 0:
                start = None
            if stop >= dim:
                stop = None
            if step == 1:
                step = None
        elif step < 0:
            if start >= dim - 1:
                start = None
            if stop < 0:
                stop = None
        return slice(start, stop, step)
    return idx
