def _arrays_to_mgr(arrays, arr_names, index, columns, dtype=None):
    """
    Segregate Series based on type and coerce into matrices.
    Needs to handle a lot of exceptional cases.
    """
    # figure out the index, if necessary
    if index is None:
        index = extract_index(arrays)
    else:
        index = _ensure_index(index)

    # don't force copy because getting jammed in an ndarray anyway
    arrays = _homogenize(arrays, index, dtype)

    # from BlockManager perspective
    axes = [_ensure_index(columns), _ensure_index(index)]

    return create_block_manager_from_arrays(arrays, arr_names, axes)
