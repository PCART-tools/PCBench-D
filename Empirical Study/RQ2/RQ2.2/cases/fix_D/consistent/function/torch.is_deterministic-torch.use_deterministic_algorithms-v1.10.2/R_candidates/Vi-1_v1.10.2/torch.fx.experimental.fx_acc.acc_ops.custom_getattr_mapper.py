@register_custom_acc_mapper_fn(
    op_and_target=("call_function", getattr),
    arg_replacement_tuples=[],
)
def custom_getattr_mapper(node: torch.fx.Node, _: nn.Module) -> torch.fx.Node:
    """
    Custom function for mapping a call_function getattr to other ops. Currently only
    supports loading a getattr called on a torch.Tensor with attr name "shape", which is
    supported by mapping it to acc_ops.size().
    """
    # Have to use args here since getattr forces positional args.
    input_obj = node.args[0]
    attr_name = node.args[1]
    assert isinstance(input_obj, torch.fx.Node)
    assert (
        input_obj.meta["type"] == torch.Tensor
    ), f"Expected torch.Tensor type for {input_obj.meta['type']}"
    assert (
        attr_name == "shape"
    ), f"Only supporting shape getattr for now, not {attr_name}"
    with node.graph.inserting_before(node):
        size_node = node.graph.call_function(size, kwargs={"input": input_obj})
        size_node.meta = node.meta.copy()
        return size_node
