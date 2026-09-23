@register_custom_acc_mapper_fn(
    op_and_target=("call_function", torch.addmm),
    arg_replacement_tuples=[
        ("input", "input"),
        ("mat1", "mat1"),
        ("mat2", "mat2"),
        ("beta", "beta"),
        ("alpha", "alpha"),
    ],
)
def addmm_mapper(node: torch.fx.Node, _: nn.Module) -> torch.fx.Node:
    """
    Mapping from torch.addmm to acc_ops.mm -> acc_ops.add, if alpha or beta is not 1
    then we also insert acc_ops.mul to the right place.
    """
    with node.graph.inserting_before(node):
        mm_kwargs = {"input": node.kwargs["mat1"], "other": node.kwargs["mat2"]}
        mm_node = node.graph.create_node(
            "call_function", matmul, kwargs=mm_kwargs, name=f"{node.name}_mm"
        )
        mm_node.meta = node.meta.copy()

        if node.kwargs["alpha"] != 1:
            mul_kwargs = {"input": mm_node, "other": node.kwargs["alpha"]}
            mm_node = node.graph.create_node(
                "call_function", mul, kwargs=mul_kwargs, name=f"{mm_node.name}_mul"
            )
        mm_node.meta = node.meta.copy()

        input_node = node.kwargs["input"]
        if node.kwargs["beta"] != 1:
            mul_kwargs = {"input": input_node, "other": node.kwargs["beta"]}
            new_input_node = node.graph.create_node(
                "call_function", mul, kwargs=mul_kwargs, name=f"{node.name}_input_mul"
            )
            assert isinstance(input_node, torch.fx.Node)
            new_input_node.meta = input_node.meta.copy()
            input_node = new_input_node

        add_kwargs = {"input": mm_node, "other": input_node}
        add_node = node.graph.create_node(
            "call_function", add, kwargs=add_kwargs, name=f"{node.name}_add"
        )
        add_node.meta = node.meta.copy()
        return add_node
