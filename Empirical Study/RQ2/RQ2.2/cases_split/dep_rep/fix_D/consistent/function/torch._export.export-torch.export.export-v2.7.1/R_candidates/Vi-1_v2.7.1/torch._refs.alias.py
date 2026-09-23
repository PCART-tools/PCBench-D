@register_decomposition(aten.alias)
def alias(a: TensorLikeType) -> TensorLikeType:
    return prims.view_of(a)
