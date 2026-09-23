@_make_elementwise_unary_reference(ELEMENTWISE_TYPE_PROMOTION_KIND.ALWAYS_BOOL)
def isinf(a: TensorLikeType) -> TensorLikeType:
    if utils.is_complex_dtype(a.dtype):
        return torch.logical_or(isinf(torch.real(a)), isinf(torch.imag(a)))
    if utils.is_float_dtype(a.dtype):
        return torch.abs(a) == float("inf")
    return torch.zeros_like(a, dtype=torch.bool)
