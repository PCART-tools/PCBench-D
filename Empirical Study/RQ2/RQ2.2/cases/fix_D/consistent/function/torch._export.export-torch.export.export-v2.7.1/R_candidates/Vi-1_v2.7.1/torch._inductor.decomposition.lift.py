@register_decomposition([aten.lift, aten.detach_])
def lift(self: torch.Tensor) -> torch.Tensor:
    return self
