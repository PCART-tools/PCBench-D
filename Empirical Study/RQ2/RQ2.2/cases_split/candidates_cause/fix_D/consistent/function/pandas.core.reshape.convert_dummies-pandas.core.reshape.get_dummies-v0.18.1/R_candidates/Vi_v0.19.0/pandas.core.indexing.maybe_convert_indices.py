def maybe_convert_indices(indices, n):
    """ if we have negative indicies, translate to postive here
    if have indicies that are out-of-bounds, raise an IndexError
    """
    if isinstance(indices, list):
        indices = np.array(indices)
        if len(indices) == 0:
            # If list is empty, np.array will return float and cause indexing
            # errors.
            return np.empty(0, dtype=np.int_)

    mask = indices < 0
    if mask.any():
        indices[mask] += n
    mask = (indices >= n) | (indices < 0)
    if mask.any():
        raise IndexError("indices are out-of-bounds")
    return indices
