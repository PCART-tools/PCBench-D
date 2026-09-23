@_make_elementwise_unary_reference(
    ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT,
)
def bessel_j1(a: TensorLikeType) -> TensorLikeType:
    return prims.bessel_j1(a)
