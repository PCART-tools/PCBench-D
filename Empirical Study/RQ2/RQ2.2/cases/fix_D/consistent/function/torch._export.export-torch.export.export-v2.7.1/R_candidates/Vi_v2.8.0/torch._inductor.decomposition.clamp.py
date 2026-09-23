@register_decomposition([aten.clamp])
@pw_cast_for_opmath_non_tensor_args
def clamp(
    x: torch.Tensor,
    min: Optional[torch.types.Number] = None,
    max: Optional[torch.types.Number] = None,
) -> torch.Tensor:
    if min is not None:
        x = x.clamp_min(min)
    if max is not None:
        x = x.clamp_max(max)
    return x
