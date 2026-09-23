@register_decomposition(aten.conj_physical)
@out_wrapper()
def conj_physical(input: TensorLikeType):
    if not utils.is_complex_dtype(input.dtype):
        return input
    return prims.conj_physical(input)
