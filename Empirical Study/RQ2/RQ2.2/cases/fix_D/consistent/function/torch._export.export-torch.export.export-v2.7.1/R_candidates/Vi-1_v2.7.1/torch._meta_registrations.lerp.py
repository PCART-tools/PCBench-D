@register_meta(aten.lerp)
@out_wrapper()
def lerp(start, end, weight):
    torch._check(
        start.dtype == end.dtype,
        lambda: f"expected dtype {start.dtype} for `end`, but got dtype {end.dtype}",
    )
    args = [start, end]
    if isinstance(weight, TensorLike):
        if weight.ndim != 0:
            torch._check(
                start.dtype == weight.dtype,
                lambda: f"expected dtype {start.dtype} for `weight`, but got dtype {weight.dtype}",
            )
        args.append(weight)
    return elementwise_meta(
        *args, type_promotion=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
    )
