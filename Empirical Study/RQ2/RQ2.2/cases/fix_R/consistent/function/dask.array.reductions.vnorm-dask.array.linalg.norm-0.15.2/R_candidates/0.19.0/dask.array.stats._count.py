def _count(x, axis=None):
    if axis is None:
        return x.size
    else:
        return x.shape[axis]
