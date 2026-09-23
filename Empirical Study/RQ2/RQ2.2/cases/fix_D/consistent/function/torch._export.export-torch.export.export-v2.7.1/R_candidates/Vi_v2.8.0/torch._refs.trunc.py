@_make_elementwise_unary_reference(
    ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
    exact_dtype=True,
)
def trunc(a):
    return prims.trunc(a)
