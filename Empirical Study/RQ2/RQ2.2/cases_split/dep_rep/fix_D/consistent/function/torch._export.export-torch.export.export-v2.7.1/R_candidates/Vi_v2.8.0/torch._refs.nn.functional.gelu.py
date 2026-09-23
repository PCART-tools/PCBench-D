@register_decomposition(aten.gelu)
@out_wrapper()
@elementwise_unary_scalar_wrapper
@elementwise_type_promotion_wrapper(
    type_promoting_args=("a",),
    type_promotion_kind=utils.ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def gelu(a: TensorLikeType, approximate: str = "none") -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.gelu
    """
    if not isinstance(a, TensorLike):
        raise RuntimeError(
            "Expected a tensor input for an elementwise unary operation!"
        )
    M_SQRT2 = 1.41421356237309504880
    M_SQRT1_2 = 0.70710678118654752440
    M_2_SQRTPI = 1.12837916709551257390
    if approximate == "tanh":
        kBeta = M_SQRT2 * M_2_SQRTPI * 0.5
        kKappa = 0.044715
        a_cube = a * a * a
        inner = kBeta * (a + kKappa * a_cube)
        return 0.5 * a * (1 + torch.tanh(inner))
    elif approximate == "none":
        kAlpha = M_SQRT1_2
        return a * 0.5 * (1 + torch.erf(a * kAlpha))
    else:
        raise RuntimeError("approximate argument must be either none or tanh.")
