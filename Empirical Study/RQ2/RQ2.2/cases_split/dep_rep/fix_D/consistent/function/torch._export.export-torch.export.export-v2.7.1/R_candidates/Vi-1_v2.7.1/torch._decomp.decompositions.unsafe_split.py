@register_decomposition(aten.unsafe_split.Tensor)
def unsafe_split(input: Tensor, split_size: int, dim: int = 0) -> tuple[Tensor, ...]:
    return aten.split.Tensor(input, split_size, dim)
