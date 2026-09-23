@register_decomposition(aten.special_log_ndtr)
@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("a",),
    type_promotion_kind=utils.ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT,
)
def log_ndtr(a: TensorLikeType) -> TensorLikeType:
    # Note: M_SQRT1_2 is the value of 1 / sqrt(2)
    M_SQRT1_2 = 0.707106781186547524400844362104849039
    t = a * M_SQRT1_2
    return torch.where(
        a < 1.0,
        torch.log(torch.special.erfcx(-t) / 2) - t * t,
        torch.log1p(-torch.erfc(t) / 2),
    )
