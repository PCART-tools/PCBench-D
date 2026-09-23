def broadcast_to(a: TensorLikeType, size: ShapeType) -> TensorLikeType:
    start = len(size) - len(a.shape)
    dims = tuple(range(start, len(a.shape) + start))
    return prims.broadcast_in_dim(a, size, dims)
