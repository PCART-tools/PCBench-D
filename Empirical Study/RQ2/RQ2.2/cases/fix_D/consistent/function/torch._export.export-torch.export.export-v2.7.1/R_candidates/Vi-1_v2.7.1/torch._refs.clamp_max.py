@register_decomposition(aten.clamp_max)
@out_wrapper()
def clamp_max(
    self: TensorLikeType,
    max: Optional[TensorOrNumberLikeType] = None,
) -> TensorLikeType:
    return torch.clamp(self, max=max)  # type: ignore[arg-type]
