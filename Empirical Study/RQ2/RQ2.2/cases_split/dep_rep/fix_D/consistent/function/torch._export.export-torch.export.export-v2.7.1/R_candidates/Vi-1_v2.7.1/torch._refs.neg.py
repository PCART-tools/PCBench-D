@_make_elementwise_unary_reference(
    ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT, extra_meta=_neg_meta
)
def neg(a):
    return prims.neg(a)
