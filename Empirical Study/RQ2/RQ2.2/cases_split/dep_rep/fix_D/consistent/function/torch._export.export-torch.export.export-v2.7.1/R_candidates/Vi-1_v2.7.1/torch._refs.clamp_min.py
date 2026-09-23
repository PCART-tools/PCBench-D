@register_decomposition(aten.clamp_min)
@out_wrapper()
def clamp_min(
    self: TensorLikeType,
    min: Optional[TensorOrNumberLikeType] = None,
) -> TensorLikeType:
    return torch.clamp(self, min=min)  # type: ignore[arg-type]
