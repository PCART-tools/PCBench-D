@register_decomposition(aten.randint.default)
def randint(
    high: int,
    size: list[Union[int, torch.SymInt]],
    **kwargs: Any,
) -> torch.Tensor:
    return aten.randint.low(0, high, size, **kwargs)
