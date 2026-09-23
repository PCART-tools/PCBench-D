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
def sum_mapper(node: torch.fx.Node, mod: torch.fx.GraphModule) -> torch.fx.Node:
    return reduce_op_mapper(node, mod, sum)
