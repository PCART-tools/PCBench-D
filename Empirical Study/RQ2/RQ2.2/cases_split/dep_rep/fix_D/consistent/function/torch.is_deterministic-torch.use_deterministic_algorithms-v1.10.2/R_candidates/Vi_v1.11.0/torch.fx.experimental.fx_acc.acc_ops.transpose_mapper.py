@register_custom_acc_mapper_fn(
    op_and_target=("call_function", torch.transpose),
    arg_replacement_tuples=[
        ("input", "input"),
        ("dim0", "dim0"),
        ("dim1", "dim1"),
    ],
)
@register_custom_acc_mapper_fn(
    op_and_target=("call_method", "transpose"),
    arg_replacement_tuples=[
        ("input", "input"),
        ("dim0", "dim0"),
        ("dim1", "dim1"),
    ],
)
def transpose_mapper(node: torch.fx.Node, _: nn.Module) -> torch.fx.Node:
    # Get the dim-permutation/shuffle
    shape_as_list = node.meta["tensor_meta"].shape
    ranks = len(shape_as_list)
    shuffle = list(i for i in range(ranks))
    dim0 = cast(int, node.kwargs["dim0"])
    dim1 = cast(int, node.kwargs["dim1"])
    shuffle[dim0] = dim1
    shuffle[dim1] = dim0

    # Create the new acc_ops.permute node. Update all uses of the transpose
    # node and then delete the transpose node.
    with node.graph.inserting_after(node):
        permute_node = node.graph.call_function(
            the_function=permute,
            kwargs={
                "input": node.kwargs.get("input"),
                "permutation": shuffle,
            },
        )
        permute_node.meta = node.meta.copy()
        node.replace_all_uses_with(permute_node)

    permute_node.graph.erase_node(node)
    return permute_node
