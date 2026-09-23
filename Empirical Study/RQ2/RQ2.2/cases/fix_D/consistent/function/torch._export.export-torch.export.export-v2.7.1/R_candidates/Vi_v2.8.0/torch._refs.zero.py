@register_decomposition(aten.zero)
@out_wrapper()
def zero(input: TensorLikeType) -> TensorLikeType:
    return torch.zeros_like(input)
