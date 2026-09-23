def unflatten(a: TensorLikeType, dim: int, sizes: ShapeType) -> TensorLikeType:
    dim = utils.canonicalize_dim(a.ndim, dim)
    torch._check(len(sizes) != 0, lambda: "unflatten: sizes must be non-empty")
    return a.view(tuple(a.shape[:dim]) + tuple(sizes) + tuple(a.shape[dim + 1 :]))
