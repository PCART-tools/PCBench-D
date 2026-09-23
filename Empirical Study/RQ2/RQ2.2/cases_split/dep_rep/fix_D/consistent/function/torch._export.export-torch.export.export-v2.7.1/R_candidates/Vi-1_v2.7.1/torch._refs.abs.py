@_make_elementwise_unary_reference(
    ELEMENTWISE_TYPE_PROMOTION_KIND.COMPLEX_TO_FLOAT,
    exact_dtype=True,
)
def abs(a):
    return prims.abs(a)
