def get_attr(node: torch.fx.Node) -> Any:
    """
    Returns the underlying attr for a given node which
    must be of type get_attr.
    """
    assert node.op == "get_attr", "Expected a get_attr node"
    return get_target_from_module(node.graph.owning_module, str(node.target))
