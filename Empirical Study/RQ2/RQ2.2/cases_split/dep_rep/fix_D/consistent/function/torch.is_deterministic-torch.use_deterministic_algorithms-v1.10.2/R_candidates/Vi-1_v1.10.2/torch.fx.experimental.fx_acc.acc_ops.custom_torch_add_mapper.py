@register_custom_acc_mapper_fn(
    op_and_target=("call_function", torch.add),
    # Note that we may have aliases for inputs here due to issues with deterministically
    # knowing the correct target that will be resolved by pytorch.
    arg_replacement_tuples=[
        (("input", "a"), "input"),
        (("other", "b"), "other"),
        ("alpha", "alpha", this_arg_is_optional),
    ],
)
def custom_torch_add_mapper(node: torch.fx.Node, mod: nn.Module) -> torch.fx.Node:
    """
    Add custom mapping for torch.add because it has an `alpha` parameter which scales
    the `other` input, and we want to make that mul a separate node.
    """
    with node.graph.inserting_before(node):
        # If alpha is in kwargs check if we need to add a mul, and use correct kwargs.
        if "alpha" in node.kwargs:
            # Add mul node only if it has a numerical impact, i.e. alpha != 1.0.
            if node.kwargs["alpha"] != 1.0:
                other_node = node.graph.create_node(
                    "call_function",
                    mul,
                    kwargs={
                        "input": node.kwargs["other"],
                        "other": node.kwargs["alpha"],
                    },
                    name=node.name + "_mul_alpha",
                )
                other_node.meta = node.meta
            else:
                other_node = node.kwargs["other"]
            add_kwargs = {"input": node.kwargs["input"], "other": other_node}
        else:
            add_kwargs = node.kwargs

        new_node = node.graph.create_node(
            "call_function", add, kwargs=add_kwargs, name=node.name
        )
        new_node.meta = node.meta
        return new_node
