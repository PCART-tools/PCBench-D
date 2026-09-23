def _vindex_transpose(block, axis):
    """ Rotate block so that points are on the first dimension """
    axes = [axis] + list(range(axis)) + list(range(axis + 1, block.ndim))
    return block.transpose(axes)
