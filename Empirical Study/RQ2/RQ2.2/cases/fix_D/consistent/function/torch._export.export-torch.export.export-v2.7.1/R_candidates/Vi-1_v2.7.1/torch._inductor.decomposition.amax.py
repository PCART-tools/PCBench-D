@register_decomposition(aten.amax)
def amax(
    self: torch.Tensor,
    dim: Optional[int] = None,
    keepdim: bool = False,
) -> torch.Tensor:
    if self.dtype == torch.bool:
        return torch.any(self, dim=dim, keepdim=keepdim)
    return NotImplemented
