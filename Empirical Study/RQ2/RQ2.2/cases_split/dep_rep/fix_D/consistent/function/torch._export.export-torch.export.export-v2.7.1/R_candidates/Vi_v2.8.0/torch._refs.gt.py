@_make_elementwise_binary_reference(
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.ALWAYS_BOOL,
    supports_lhs_python_scalar=False,
)
def gt(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.gt(a, b)
