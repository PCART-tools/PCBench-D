def size(a: ArrayLike, axis=None):
    if axis is None:
        return a.numel()
    else:
        return a.shape[axis]
