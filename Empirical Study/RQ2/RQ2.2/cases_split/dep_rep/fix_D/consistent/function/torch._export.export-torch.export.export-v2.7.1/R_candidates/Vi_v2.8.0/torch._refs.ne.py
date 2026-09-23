@_make_elementwise_binary_reference(
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.ALWAYS_BOOL,
    supports_lhs_python_scalar=False,
)
def ne(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.ne(a, b)
