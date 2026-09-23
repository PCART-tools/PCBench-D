@_make_elementwise_binary_reference(
    type_promotion_kind=utils.ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT,
)
def zeta(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.zeta(a, b)
