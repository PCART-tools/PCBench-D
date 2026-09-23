@_make_elementwise_binary_reference(
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def maximum(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.maximum(a, b)
