@register_decomposition([aten.fmin, prims.fmin])
def fmin(self: torch.Tensor, other: torch.Tensor) -> torch.Tensor:
    return torch.where(torch.isnan(other) | (other > self), self, other)
