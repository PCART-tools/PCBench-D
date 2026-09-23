@register_decomposition(aten.silu)
@out_wrapper()
@pw_cast_for_opmath
def silu(self: Tensor) -> Tensor:
    return self * torch.sigmoid(self)
