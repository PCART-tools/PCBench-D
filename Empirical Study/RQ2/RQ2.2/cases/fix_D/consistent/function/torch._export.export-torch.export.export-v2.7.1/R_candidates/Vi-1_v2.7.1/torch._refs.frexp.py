@register_decomposition(aten.frexp)
@out_wrapper("mantissa", "exponent")
def frexp(self: TensorLikeType) -> tuple[TensorLikeType, TensorLikeType]:
    return torch.return_types.frexp(prims.frexp(self))
