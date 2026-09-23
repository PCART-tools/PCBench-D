@_make_elementwise_unary_reference(ELEMENTWISE_TYPE_PROMOTION_KIND.ALWAYS_BOOL)
def logical_not(a: TensorLikeType):
    if not utils.is_boolean_dtype(a.dtype):
        return a == 0
    return ~a
