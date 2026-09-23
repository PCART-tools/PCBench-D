def get_arg_target_dtype_as_input_to_node(
    arg: Node,
    node: Node,
    modules: Dict[str, torch.nn.Module],
    node_name_to_target_dtype: Dict[str, Dict[str, Optional[torch.dtype]]],
) -> Optional[torch.dtype]:
    """ Get the target argument dtype for the argument `arg`, as input
    to node `node`
    """
    assert isinstance(arg, Node)
    is_weight = node_arg_is_weight(node, arg)
    is_bias = node_arg_is_bias(node, arg)
    is_activation = not is_weight and not is_bias
    if is_activation:
        return node_name_to_target_dtype[node.name]["input_activation_dtype"]
    elif is_weight:
        if node.target in NON_QUANTIZABLE_WEIGHT_OPS:
            return None
        else:
            return node_name_to_target_dtype[node.name]["weight_dtype"]
    else:
        return node_name_to_target_dtype[node.name]["bias_dtype"]
