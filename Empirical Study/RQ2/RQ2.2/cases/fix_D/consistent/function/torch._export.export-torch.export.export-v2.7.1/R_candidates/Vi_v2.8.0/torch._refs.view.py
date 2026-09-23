@register_decomposition(aten.view.default)
def view(a: TensorLikeType, *shape: ShapeType) -> TensorLikeType:
    return _reshape_view_helper(a, *shape, allow_copy=False)
