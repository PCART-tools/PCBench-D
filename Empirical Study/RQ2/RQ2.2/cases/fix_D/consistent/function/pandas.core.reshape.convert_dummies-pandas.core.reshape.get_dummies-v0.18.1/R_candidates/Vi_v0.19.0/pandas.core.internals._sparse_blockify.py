def _sparse_blockify(tuples, dtype=None):
    """ return an array of blocks that potentially have different dtypes (and
    are sparse)
    """

    new_blocks = []
    for i, names, array in tuples:
        array = _maybe_to_sparse(array)
        block = make_block(array, klass=SparseBlock, fastpath=True,
                           placement=[i])
        new_blocks.append(block)

    return new_blocks
