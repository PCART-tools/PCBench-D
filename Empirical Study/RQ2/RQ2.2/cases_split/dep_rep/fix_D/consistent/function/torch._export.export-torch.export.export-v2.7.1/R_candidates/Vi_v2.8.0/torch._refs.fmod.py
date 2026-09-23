@_make_elementwise_binary_reference(
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
    supports_lhs_python_scalar=False,
    supports_rhs_python_scalar=True,
)
def fmod(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.fmod(a, b)
