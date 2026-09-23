@register_custom_acc_mapper_fn(
    op_and_target=("call_function", torch.argmin),
    arg_replacement_tuples=[
        ("input", "input"),
        ("dim", "dim"),
        ("keepdim", "keepdim"),
    ],
)
def torch_argmin_mapper(node: torch.fx.Node, _: torch.nn.Module) -> torch.fx.Node:
    """
    Map torch.argmin to acc_ops.flatten (depend on dim) + acc_ops.topk + acc_ops.getitem
    + acc_ops.squeeze (depends on keepdim).
    """
    return argmin_max_mapper_impl(node, largest=False)
