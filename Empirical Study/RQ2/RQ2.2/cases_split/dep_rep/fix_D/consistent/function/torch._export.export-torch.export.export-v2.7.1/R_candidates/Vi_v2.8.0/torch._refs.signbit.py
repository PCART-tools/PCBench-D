@_make_elementwise_unary_reference(
    ELEMENTWISE_TYPE_PROMOTION_KIND.ALWAYS_BOOL,
    exact_dtype=True,
)
def signbit(a):
    return prims.signbit(a)
