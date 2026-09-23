@register_decomposition([aten.conj_physical])
def conj_physical(self: torch.Tensor) -> torch.Tensor:
    if self.is_complex():
        return NotImplemented
    return self
