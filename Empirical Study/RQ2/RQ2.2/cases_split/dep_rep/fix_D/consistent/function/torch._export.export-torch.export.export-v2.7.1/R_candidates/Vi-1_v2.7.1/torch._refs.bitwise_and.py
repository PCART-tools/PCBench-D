@_make_elementwise_binary_reference(
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def bitwise_and(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.bitwise_and(a, b)
