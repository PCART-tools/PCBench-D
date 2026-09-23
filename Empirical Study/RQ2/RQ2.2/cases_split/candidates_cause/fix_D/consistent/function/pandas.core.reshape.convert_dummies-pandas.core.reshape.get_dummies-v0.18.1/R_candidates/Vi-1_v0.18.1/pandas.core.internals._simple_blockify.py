def _simple_blockify(tuples, dtype):
    """ return a single array of a block that has a single dtype; if dtype is
    not None, coerce to this dtype
    """
    values, placement = _stack_arrays(tuples, dtype)

    # CHECK DTYPE?
    if dtype is not None and values.dtype != dtype:  # pragma: no cover
        values = values.astype(dtype)

    block = make_block(values, placement=placement)
    return [block]
