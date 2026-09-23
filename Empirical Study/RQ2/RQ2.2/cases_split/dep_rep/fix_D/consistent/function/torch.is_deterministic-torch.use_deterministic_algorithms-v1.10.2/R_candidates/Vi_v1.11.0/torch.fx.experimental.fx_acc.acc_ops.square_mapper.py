@register_custom_acc_mapper_fn(
    op_and_target=("call_function", torch.square),
    arg_replacement_tuples=[
        ("input", "input"),
    ],
)
def square_mapper(node: torch.fx.Node, _: nn.Module) -> torch.fx.Node:
    input_node = node.kwargs["input"]
    with node.graph.inserting_before(node):
        new_node = node.graph.call_function(
            mul, kwargs={"input": input_node, "other": input_node}
        )
        new_node.meta = node.meta.copy()
        return new_node
