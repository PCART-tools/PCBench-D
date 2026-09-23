@_make_elementwise_binary_reference(
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def remainder(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.remainder(a, b)
