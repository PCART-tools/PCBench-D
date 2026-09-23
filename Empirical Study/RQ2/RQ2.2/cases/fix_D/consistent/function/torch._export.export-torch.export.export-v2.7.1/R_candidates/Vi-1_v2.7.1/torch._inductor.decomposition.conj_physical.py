@register_decomposition([aten.conj_physical])
def conj_physical(self: torch.Tensor) -> torch.Tensor:
    assert not self.is_complex(), "TODO: implement this"
    return self
