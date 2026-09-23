def _multi_blockify(tuples, dtype=None):
    """ return an array of blocks that potentially have different dtypes """

    # group by dtype
    grouper = itertools.groupby(tuples, lambda x: x[2].dtype)

    new_blocks = []
    for dtype, tup_block in grouper:

        values, placement = _stack_arrays(list(tup_block), dtype)

        block = make_block(values, placement=placement)
        new_blocks.append(block)

    return new_blocks
