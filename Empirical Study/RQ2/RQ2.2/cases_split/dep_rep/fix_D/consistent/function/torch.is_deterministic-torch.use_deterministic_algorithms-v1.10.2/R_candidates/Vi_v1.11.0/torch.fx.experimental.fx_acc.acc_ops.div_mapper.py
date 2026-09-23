@register_custom_acc_mapper_fn(
    op_and_target=("call_function", torch.div),
    arg_replacement_tuples=[
        ("input", "input"),
        ("other", "other"),
        ("rounding_mode", "rounding_mode", this_arg_is_optional),
    ],
)
def div_mapper(node: torch.fx.Node, mod: torch.fx.GraphModule) -> torch.fx.Node:
    with node.graph.inserting_before(node):
        div_kwargs = dict(node.kwargs)
        if "rounding_mode" not in div_kwargs or div_kwargs["rounding_mode"] is None:
            div_node = node.graph.call_function(
                div, kwargs={"input": div_kwargs["input"], "other": div_kwargs["other"]}
            )
        elif div_kwargs["rounding_mode"] == "trunc":
            div_node = node.graph.call_function(
                trunc_div,
                kwargs={"input": div_kwargs["input"], "other": div_kwargs["other"]},
            )
        elif div_kwargs["rounding_mode"] == "floor":
            div_node = node.graph.call_function(
                floor_div,
                kwargs={"input": div_kwargs["input"], "other": div_kwargs["other"]},
            )
        else:
            raise RuntimeError(
                f"Unhandled div rounding mode {div_kwargs['rounding_mode']}"
            )
        div_node.meta = node.meta.copy()
        return div_node
