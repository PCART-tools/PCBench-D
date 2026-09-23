def reshape(a: TensorLikeType, *shape: ShapeType) -> TensorLikeType:
    return _reshape_view_helper(a, *shape, allow_copy=True)
