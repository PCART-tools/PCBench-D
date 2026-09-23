@register_decomposition(aten.unsafe_split_with_sizes.default)
def unsafe_split_with_sizes(
    input: Tensor, split_sizes: list[int], dim: int = 0
) -> tuple[Tensor, ...]:
    return aten.split_with_sizes.default(input, split_sizes, dim)
