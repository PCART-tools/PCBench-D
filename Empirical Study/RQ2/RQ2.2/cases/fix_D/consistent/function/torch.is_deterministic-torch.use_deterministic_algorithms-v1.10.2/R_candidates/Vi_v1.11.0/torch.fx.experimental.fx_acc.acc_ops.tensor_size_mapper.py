@register_custom_acc_mapper_fn(
    op_and_target=("call_method", "size"),
    arg_replacement_tuples=[
        ("input", "input"),
        ("dim", "dim", this_arg_is_optional),
    ],
)
def tensor_size_mapper(node: torch.fx.Node, _: nn.Module) -> torch.fx.Node:
    """
    Mapping from Tensor.size() to acc_ops.size. We map size() to acc_ops.size directly
    and map size(dim) to acc_ops.size + acc_ops.getitem.
    """

    with node.graph.inserting_before(node):
        size_node = node.graph.call_function(
            size, kwargs={"input": node.kwargs["input"]}
        )

        if "dim" not in node.kwargs:
            size_node.meta = node.meta.copy()
            return size_node

        size_node.meta["type"] = torch.Size
        getitem_node = node.graph.call_function(
            getitem, kwargs={"input": size_node, "idx": node.kwargs["dim"]}
        )
        getitem_node.meta = node.meta.copy()
        return getitem_node
