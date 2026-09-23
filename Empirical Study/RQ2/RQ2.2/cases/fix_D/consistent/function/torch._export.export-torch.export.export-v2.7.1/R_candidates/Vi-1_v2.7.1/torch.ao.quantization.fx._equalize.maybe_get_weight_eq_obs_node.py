def maybe_get_weight_eq_obs_node(
    op_node: Node, modules: dict[str, nn.Module]
) -> Optional[Node]:
    """Gets the weight equalization observer node if it exists."""
    assert op_node.op == "call_function"
    for node_arg in op_node.args:
        if node_arg_is_weight(op_node, node_arg):
            assert (
                isinstance(node_arg, Node)
                and node_arg.op == "call_module"
                and isinstance(
                    modules[str(node_arg.target)], _WeightEqualizationObserver
                )
            )
            return node_arg
    return None
