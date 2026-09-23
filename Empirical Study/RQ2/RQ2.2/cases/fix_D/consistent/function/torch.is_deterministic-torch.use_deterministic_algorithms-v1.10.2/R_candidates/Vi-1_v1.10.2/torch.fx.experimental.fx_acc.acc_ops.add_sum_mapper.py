@register_custom_acc_mapper_fn(
    op_and_target=("call_method", "sum"),
    arg_replacement_tuples=[
        ("input", "input"),
        ("dim", "dim", this_arg_is_optional),
        ("keepdim", "keepdim", this_arg_is_optional),
        ("dtype", "dtype", this_arg_is_optional),
    ],
)
@register_custom_acc_mapper_fn(
    op_and_target=("call_function", torch.sum),
    arg_replacement_tuples=[
        ("input", "input"),
        ("dim", "dim", this_arg_is_optional),
        ("keepdim", "keepdim", this_arg_is_optional),
        ("dtype", "dtype", this_arg_is_optional),
    ],
)
def add_sum_mapper(node: torch.fx.Node, mod: torch.fx.GraphModule) -> torch.fx.Node:
    with node.graph.inserting_before(node):
        sum_kwargs = dict(node.kwargs)
        if "dim" in sum_kwargs and isinstance(sum_kwargs["dim"], int):
            sum_kwargs["dim"] = (sum_kwargs["dim"],)
        sum_node = node.graph.call_function(sum, kwargs=sum_kwargs)
        sum_node.meta = node.meta.copy()
        return sum_node
