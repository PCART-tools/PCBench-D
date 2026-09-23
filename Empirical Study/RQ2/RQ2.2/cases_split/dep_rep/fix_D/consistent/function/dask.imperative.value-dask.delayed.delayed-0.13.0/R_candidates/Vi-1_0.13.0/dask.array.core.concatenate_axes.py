def concatenate_axes(arrays, axes):
    """ Recurseively call np.concatenate along axes

    TODO: This performs many copies.  We should be able to do this in one
    TODO: Merge logic on concatenate3 with this
    """
    if len(axes) != ndimlist(arrays):
        raise ValueError("Length of axes should equal depth of nested arrays")
    if len(axes) > 1:
        arrays = [concatenate_axes(a, axes[1:]) for a in arrays]
    return np.concatenate(arrays, axis=axes[0])
