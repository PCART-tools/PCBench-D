@register_custom_acc_mapper_fn(
    op_and_target=("call_method", "reshape"),
    arg_replacement_tuples=[
        ("input", "input"),
        ("*", "shape"),
    ],
)
def custom_tensor_reshape_mapper(node: torch.fx.Node, _: nn.Module) -> torch.fx.Node:
    """
    For Tensor.reshape node, args could be (input, 1, 2, 3) or (input, (1, 2, 3)).
    Here we do some special handling with the `shape` arg in order to map it to
    acc_ops.reshape. It also handles the case when `shape` is a list instead of
    tuple.
    """
    input_node = node.kwargs["input"]
    shape = node.kwargs["shape"]

    assert isinstance(shape, Sequence)
    if isinstance(shape[0], (tuple, list)):  # type: ignore[index]
        shape = shape[0]  # type: ignore[index]

    with node.graph.inserting_before(node):
        new_node = node.graph.call_function(
            reshape,
            kwargs={
                "input": input_node,
                "acc_out_ty": acc_utils.build_raw_tensor_meta(shape=shape),
            },
        )
        new_node.meta = node.meta.copy()
        return new_node
