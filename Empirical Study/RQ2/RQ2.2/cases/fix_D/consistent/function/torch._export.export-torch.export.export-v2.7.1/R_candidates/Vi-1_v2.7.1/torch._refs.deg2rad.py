@_make_elementwise_unary_reference(ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT)
def deg2rad(self: TensorLikeType):
    torch._check(
        not utils.is_complex_dtype(self.dtype),
        lambda: "deg2rad is not supported for complex tensors.",
    )
    M_PI_180 = 0.017453292519943295769236907684886127134428718885417
    return self * M_PI_180
