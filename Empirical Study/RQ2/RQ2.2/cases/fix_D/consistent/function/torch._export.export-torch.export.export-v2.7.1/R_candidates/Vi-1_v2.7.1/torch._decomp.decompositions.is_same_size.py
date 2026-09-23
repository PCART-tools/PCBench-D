@register_decomposition(aten.is_same_size.default)
def is_same_size(a: Tensor, b: Tensor) -> bool:
    return a.shape == b.shape
