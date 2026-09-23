@_make_elementwise_unary_reference(
    ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT,
)
def spherical_bessel_j0(a: TensorLikeType) -> TensorLikeType:
    return prims.spherical_bessel_j0(a)
