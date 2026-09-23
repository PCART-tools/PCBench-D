def maybe_get_weight_eq_obs_node(op_node: Node, modules: Dict[str, nn.Module]) -> Optional[Node]:
    """ Gets the weight equalization observer node if it exists.
    """
    assert(op_node.op == 'call_function' and op_node.target in WEIGHT_INDEX_DICT)
    for i, node_arg in enumerate(op_node.args):
        if i in WEIGHT_INDEX_DICT[op_node.target]:  # type: ignore[index]
            assert(isinstance(node_arg, Node) and node_arg.op == 'call_module' and
                   isinstance(modules[str(node_arg.target)], _WeightEqualizationObserver))
            return node_arg
    return None
