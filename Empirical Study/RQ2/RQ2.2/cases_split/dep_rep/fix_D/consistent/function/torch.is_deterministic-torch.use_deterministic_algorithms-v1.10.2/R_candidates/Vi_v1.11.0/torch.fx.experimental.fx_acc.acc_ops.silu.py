@register_custom_acc_mapper_fn(
    op_and_target=("call_function", nn.functional.silu),
    arg_replacement_tuples=[
        ("input", "input"),
    ],
)
def silu(node: torch.fx.Node, _: nn.Module) -> torch.fx.Node:
    input_node = node.kwargs["input"]
    with node.graph.inserting_before(node):
        sigmoid_node = node.graph.call_function(sigmoid, kwargs={"input": input_node})
        sigmoid_node.meta = node.meta.copy()
        new_node = node.graph.call_function(
            mul, kwargs={"input": sigmoid_node, "other": input_node}
        )
        new_node.meta = node.meta.copy()
        return new_node
