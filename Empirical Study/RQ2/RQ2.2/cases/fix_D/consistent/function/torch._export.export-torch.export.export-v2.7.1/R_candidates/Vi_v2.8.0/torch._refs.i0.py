@_make_elementwise_unary_reference(
    ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT, aten_op=aten.i0
)
def i0(a):
    return prims.bessel_i0(a)
