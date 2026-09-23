@_make_elementwise_unary_reference(
    ELEMENTWISE_TYPE_PROMOTION_KIND.ALWAYS_BOOL,
    aten_op=None,  # CompositeImplicitAutograd
)
def isreal(a: TensorLikeType) -> TensorLikeType:
    if utils.is_complex_dtype(a.dtype):
        return torch.imag(a) == 0
    return torch.ones_like(a, dtype=torch.bool)
