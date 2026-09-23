@register_lowering_pattern(
    CallFunction(
        aten.scatter.value,
        CallFunction(
            aten.full,
            KeywordArg("shape"),
            KeywordArg("background_val"),
            dtype=KeywordArg("dtype"),
        ),
        KeywordArg("dim"),
        KeywordArg("selector"),
        KeywordArg("val"),  # scalar value
    ),
    extra_check=scatter_upon_const_tensor_extra_check,
)
def scatter_upon_const_tensor(
    match: Match, shape, background_val, dtype, dim, selector, val
):
    """
    Match the pattern of full+scatter into a pointwise.

    TODO: Right now the scatter value must be a scalar. But we could support it
    when it is a tensor as well.
    """
    from torch._inductor import metrics

    metrics.num_matches_for_scatter_upon_const_tensor += 1

    selector_loader = selector.make_loader()

    def inner_fn(idx):
        selector_idx = list(idx)
        selector_idx[dim] = 0

        selector = selector_loader(selector_idx)
        return ops.where(
            selector == ops.index_expr(idx[dim], torch.int64),
            ops.constant(val, dtype),
            ops.constant(background_val, dtype),
        )

    return ir.Pointwise.create(
        device=selector.get_device(),
        dtype=dtype,
        inner_fn=inner_fn,
        ranges=shape,
    )
