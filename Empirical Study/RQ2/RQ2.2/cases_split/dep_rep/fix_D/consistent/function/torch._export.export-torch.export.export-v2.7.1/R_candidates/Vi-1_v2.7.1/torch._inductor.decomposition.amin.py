@register_decomposition(aten.amin)
def amin(
    self: torch.Tensor,
    dim: Optional[int] = None,
    keepdim: bool = False,
) -> torch.Tensor:
    if self.dtype == torch.bool:
        return torch.all(self, dim=dim, keepdim=keepdim)
    return NotImplemented
