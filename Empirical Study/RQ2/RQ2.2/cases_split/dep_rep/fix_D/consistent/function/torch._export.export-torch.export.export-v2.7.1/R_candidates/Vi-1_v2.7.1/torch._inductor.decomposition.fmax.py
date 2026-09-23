@register_decomposition([aten.fmax, prims.fmax])
def fmax(self: torch.Tensor, other: torch.Tensor) -> torch.Tensor:
    return torch.where(torch.isnan(other) | (other < self), self, other)
