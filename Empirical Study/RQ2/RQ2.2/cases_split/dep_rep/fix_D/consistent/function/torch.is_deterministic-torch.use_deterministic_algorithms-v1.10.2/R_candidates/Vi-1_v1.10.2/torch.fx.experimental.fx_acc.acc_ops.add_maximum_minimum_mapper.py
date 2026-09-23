@register_custom_acc_mapper_fn(
    op_and_target=("call_method", "max"),
    arg_replacement_tuples=[
        ("input", "input"),
        (("dim", "other"), "dim_or_other", this_arg_is_optional),
        ("keepdim", "keepdim", this_arg_is_optional),
    ],
)
@register_custom_acc_mapper_fn(
    op_and_target=("call_function", torch.max),
    arg_replacement_tuples=[
        ("input", "input"),
        (("dim", "other"), "dim_or_other", this_arg_is_optional),
        ("keepdim", "keepdim", this_arg_is_optional),
    ],
)
@register_custom_acc_mapper_fn(
    op_and_target=("call_method", "min"),
    arg_replacement_tuples=[
        ("input", "input"),
        (("dim", "other"), "dim_or_other", this_arg_is_optional),
        ("keepdim", "keepdim", this_arg_is_optional),
    ],
)
@register_custom_acc_mapper_fn(
    op_and_target=("call_function", torch.min),
    arg_replacement_tuples=[
        ("input", "input"),
        (("dim", "other"), "dim_or_other", this_arg_is_optional),
        ("keepdim", "keepdim", this_arg_is_optional),
    ],
)
def add_maximum_minimum_mapper(
    node: torch.fx.Node, mod: torch.fx.GraphModule
) -> torch.fx.Node:
    # there are effectively three versions of torch.max / torch.min
    # full reduce: torch.max(input) -> Tensor
    # dimensional reduce: torch.max(input, dim, keepdim=False, *, out=None) -> (Tensor, LongTensor)
    # elementwise: torch.max(input, other, *, out=None) -> Tensor

    # the mapper function is remapping for both min and max situations
    # this helper function makes the choices available clearer and provides an easier way
    # to lookup the right function
    def target_map(op, target):
        if (op, target) in (("call_method", "max"), ("call_function", torch.max)):
            return dict(
                full_reduce=max_full_reduce,
                dim_reduce=max_dim_reduce,
                elementwise=maximum,
            )
        elif (op, target) in (("call_method", "min"), ("call_function", torch.min)):
            return dict(
                full_reduce=min_full_reduce,
                dim_reduce=min_dim_reduce,
                elementwise=minimum,
            )

    with node.graph.inserting_before(node):
        new_targets = target_map(node.op, node.target)
        max_kwargs = dict()
        max_kwargs["input"] = node.kwargs["input"]
        if ("dim_or_other" not in node.kwargs) or (node.kwargs["dim_or_other"] is None):
            nt = new_targets["full_reduce"]
            max_node = node.graph.call_function(nt, kwargs=max_kwargs)
        elif isinstance(node.kwargs["dim_or_other"], int):
            nt = new_targets["dim_reduce"]
            dim = node.kwargs["dim_or_other"]
            max_kwargs["dim"] = dim
            max_kwargs["keepdim"] = node.kwargs.get("keepdim", False)
            max_node = node.graph.call_function(nt, kwargs=max_kwargs)
        else:
            other = node.kwargs["dim_or_other"]
            assert isinstance(other, torch.fx.Node)
            # Lowering path for when provided "other", where we do elem-wise max
            nt = new_targets["elementwise"]
            max_kwargs["other"] = other
            max_node = node.graph.call_function(nt, kwargs=max_kwargs)
        max_node.meta = node.meta.copy()
        return max_node
