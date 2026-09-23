@_make_elementwise_unary_reference(
    ELEMENTWISE_TYPE_PROMOTION_KIND.ALWAYS_BOOL,
    exact_dtype=True,
)
def isposinf(a: TensorLikeType) -> TensorLikeType:
    torch._check(
        not utils.is_complex_dtype(a.dtype),
        lambda: f"Complex dtype is not supported for isposinf, got dtype {a.dtype}",
    )
    if utils.is_float_dtype(a.dtype):
        return a == float("inf")
    return torch.zeros_like(a, dtype=torch.bool)
