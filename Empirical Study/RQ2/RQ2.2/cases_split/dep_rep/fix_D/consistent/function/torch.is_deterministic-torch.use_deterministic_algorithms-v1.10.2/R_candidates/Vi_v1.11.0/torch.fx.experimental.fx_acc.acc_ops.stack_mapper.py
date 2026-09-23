@register_custom_acc_mapper_fn(
    op_and_target=("call_function", torch.stack),
    arg_replacement_tuples=[
        ("tensors", "tensors"),
        ("dim", "dim"),
    ],
)
def stack_mapper(node: torch.fx.Node, _: nn.Module) -> torch.fx.Node:
    """
    Map torch.stack to unsqueeze + cat.
    """
    with node.graph.inserting_before(node):
        inputs = node.kwargs["tensors"]
        unsqueeze_nodes = []
        assert isinstance(inputs, Sequence)
        for i, t in enumerate(inputs):
            new_node = node.graph.create_node(
                "call_function",
                unsqueeze,
                kwargs={"input": t, "dim": node.kwargs["dim"]},
                name=f"{node.name}_unsqueeze_{i}",
            )
            new_node.meta["type"] = torch.Tensor
            unsqueeze_nodes.append(new_node)
        cat_node = node.graph.create_node(
            "call_function",
            cat,
            kwargs={"tensors": unsqueeze_nodes, "dim": node.kwargs["dim"]},
        )
        cat_node.meta = node.meta.copy()
        return cat_node
