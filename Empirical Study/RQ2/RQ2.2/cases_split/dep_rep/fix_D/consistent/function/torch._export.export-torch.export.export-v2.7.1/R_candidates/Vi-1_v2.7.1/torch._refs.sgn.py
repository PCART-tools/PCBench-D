@_make_elementwise_unary_reference(
    ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
    exact_dtype=True,
)
def sgn(a):
    if utils.is_complex_dtype(a.dtype):
        a_abs = a.abs()
        return torch.where(a_abs == 0, 0, a / a_abs)
    else:
        return a.sign()
