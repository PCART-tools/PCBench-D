@register_decomposition(aten.masked_fill_)
def masked_fill_(
    a: TensorLikeType, mask: TensorLikeType, value: TensorOrNumberLikeType
) -> TensorLikeType:
    b = torch.masked_fill(a, mask, value)  # type: ignore[arg-type]
    a.copy_(b)
    return a
