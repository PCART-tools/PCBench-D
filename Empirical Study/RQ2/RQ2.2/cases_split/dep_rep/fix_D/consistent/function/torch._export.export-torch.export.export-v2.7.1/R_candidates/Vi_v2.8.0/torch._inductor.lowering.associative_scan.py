@register_lowering(associative_scan_op, type_promotion_kind=None)
def associative_scan(
    combine_fn: ir.Subgraph, xs, additional_inputs: tuple[torch.Tensor]
):
    from .subgraph_lowering import InputDescriptor, lower_pointwise_subgraph

    if len(additional_inputs) > 0:
        raise RuntimeError(
            "Unable to generate code for associative_scan op, because there are lifted arguments"
        )

    subgraph_inputs = [
        InputDescriptor(dtype=x.get_dtype(), device=x.get_device())
        for x in itertools.chain(xs, xs)
    ]
    lowered_combine_fn = lower_pointwise_subgraph(combine_fn, subgraph_inputs)  # type: ignore[var-annotated]

    def wrapped_combine_fn(lhs, rhs):
        return lowered_combine_fn(
            *pytree.tree_leaves(lhs),
            *pytree.tree_leaves(rhs),
        )

    kwargs = _make_scan_inner(xs[0], axis=0, dtype=None)
    kwargs["dtypes"] = tuple(x.get_dtype() for x in xs)
    kwargs["inner_fns"] = tuple(x.make_loader() for x in xs)
    result = ir.Scan.create(
        combine_fn=wrapped_combine_fn,
        can_fallback_to_aten=False,
        **kwargs,
    )
    if result[0] is None:
        raise RuntimeError("Unable to generate code for associative_scan op")
    return result
