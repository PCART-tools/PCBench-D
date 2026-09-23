@_make_elementwise_unary_reference(ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT)
def rad2deg(self: TensorLikeType):
    torch._check(
        not utils.is_complex_dtype(self.dtype),
        lambda: "rad2deg is not supported for complex tensors.",
    )
    M_180_PI = 57.295779513082320876798154814105170332405472466564
    return self * M_180_PI
