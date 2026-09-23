@_make_elementwise_binary_reference(
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
    supports_two_python_scalars=True,
)
def mul(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.mul(a, b)
