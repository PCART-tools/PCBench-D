@register_decomposition(aten.is_complex)
def is_complex(input: TensorLikeType):
    return utils.is_complex_dtype(input.dtype)
