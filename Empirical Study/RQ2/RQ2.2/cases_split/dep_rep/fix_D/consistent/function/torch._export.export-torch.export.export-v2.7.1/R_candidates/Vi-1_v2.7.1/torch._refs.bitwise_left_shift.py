@_make_elementwise_binary_reference(
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def bitwise_left_shift(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.shift_left(a, b)
