@_make_elementwise_binary_reference(
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def minimum(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.minimum(a, b)
