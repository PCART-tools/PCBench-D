def _vindex_slice(block, points):
    """ Pull out point-wise slices from block """
    points = [p if isinstance(p, slice) else list(p) for p in points]
    return block[tuple(points)]
