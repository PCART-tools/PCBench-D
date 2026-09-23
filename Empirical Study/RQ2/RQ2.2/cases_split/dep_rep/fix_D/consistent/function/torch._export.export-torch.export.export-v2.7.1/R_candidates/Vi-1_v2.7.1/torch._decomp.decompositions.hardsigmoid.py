@register_decomposition(aten.hardsigmoid)
@out_wrapper()
@pw_cast_for_opmath
def hardsigmoid(self: Tensor) -> Tensor:
    return torch.clamp(torch.clamp(self + 3, min=0), max=6) / 6
