@register_decomposition(aten.round)
@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("a",),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def round(a: TensorLikeType, *, decimals: int = 0) -> TensorLikeType:
    if decimals == 0:
        return prims.round(a)
    else:
        ten_pow = 10**decimals
        ten_neg_pow = 10 ** (-decimals)
        return prims.mul(prims.round(prims.mul(a, ten_pow)), ten_neg_pow)
