@register_decomposition(aten.special_erfcx)
@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("a",),
    type_promotion_kind=utils.ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT,
)
def erfcx(a: TensorLikeType) -> TensorLikeType:
    return prims.erfcx(a)
