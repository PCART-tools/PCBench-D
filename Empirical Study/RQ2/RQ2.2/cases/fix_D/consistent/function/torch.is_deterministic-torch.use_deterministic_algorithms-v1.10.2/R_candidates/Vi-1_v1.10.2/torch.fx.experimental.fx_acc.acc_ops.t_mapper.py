@register_custom_acc_mapper_fn(
    op_and_target=("call_function", torch.t),
    arg_replacement_tuples=[
        ("input", "input"),
    ],
)
@register_custom_acc_mapper_fn(
    op_and_target=("call_method", "t"),
    arg_replacement_tuples=[
        ("input", "input"),
    ],
)
def t_mapper(node: torch.fx.Node, _: nn.Module):
    ranks = len(node.meta["tensor_meta"].shape)
    shuffle = [1, 0] if (ranks > 1) else [0]

    with node.graph.inserting_before(node):
        new_node = node.graph.create_node(
            "call_function",
            permute,
            kwargs={"input": node.kwargs["input"], "permutation": shuffle},
        )
        new_node.meta = node.meta.copy()
        return new_node
