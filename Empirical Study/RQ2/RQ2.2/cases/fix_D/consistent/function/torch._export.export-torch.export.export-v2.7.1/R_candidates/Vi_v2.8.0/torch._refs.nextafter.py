@_make_elementwise_binary_reference(
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.NO_OPMATH,
    supports_lhs_python_scalar=False,
    supports_rhs_python_scalar=False,
)
def nextafter(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.nextafter(a, b)
