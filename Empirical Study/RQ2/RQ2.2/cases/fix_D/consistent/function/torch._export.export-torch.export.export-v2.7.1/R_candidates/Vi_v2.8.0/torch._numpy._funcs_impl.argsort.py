def argsort(a: ArrayLike, axis=-1, kind=None, order: NotImplementedType = None):
    a, axis, stable = _sort_helper(a, axis, kind, order)
    return torch.argsort(a, dim=axis, stable=stable)
