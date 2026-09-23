@_make_elementwise_binary_reference(
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def bitwise_or(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.bitwise_or(a, b)
