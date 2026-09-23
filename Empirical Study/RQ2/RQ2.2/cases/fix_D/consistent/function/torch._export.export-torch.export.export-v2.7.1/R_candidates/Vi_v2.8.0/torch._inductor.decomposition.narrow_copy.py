@register_decomposition([aten.narrow_copy])
def narrow_copy(
    self: torch.Tensor,
    dim: int,
    start: int,
    length: int,
) -> torch.Tensor:
    return torch.narrow(self, dim, start, length).clone()
