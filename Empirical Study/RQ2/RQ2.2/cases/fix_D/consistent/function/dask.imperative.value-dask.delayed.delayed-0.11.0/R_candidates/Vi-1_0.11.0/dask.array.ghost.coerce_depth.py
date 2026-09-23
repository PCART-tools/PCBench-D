def coerce_depth(ndim, depth):
    if isinstance(depth, int):
        depth = (depth,) * ndim
    if isinstance(depth, tuple):
        depth = dict(zip(range(ndim), depth))
    return depth
