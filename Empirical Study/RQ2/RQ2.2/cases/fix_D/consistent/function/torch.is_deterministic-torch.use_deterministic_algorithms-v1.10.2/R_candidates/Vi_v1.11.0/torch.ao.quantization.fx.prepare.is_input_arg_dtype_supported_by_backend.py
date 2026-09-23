def is_input_arg_dtype_supported_by_backend(
    arg: Argument,
    node: Node,
    node_name_to_target_dtype: Dict[str, Dict[str, Optional[torch.dtype]]],
    dtype_config: Dict[str, torch.dtype],
) -> bool:
    """ Check if the configured qconfig for the argument
    is supported by the backend or not
    """
    if isinstance(arg, (list, tuple)):
        return all(map(lambda a: is_input_arg_dtype_supported_by_backend(a, node, node_name_to_target_dtype, dtype_config), arg))
    if not isinstance(arg, Node):
        return True
    # TODO: support check for standalone module
    is_weight = node_arg_is_weight(node, arg)
    is_bias = node_arg_is_bias(node, arg)
    is_activation = not is_weight and not is_bias
    if is_activation:
        input_activation_dtype = dtype_config.get("input_activation_dtype", None)
        return input_activation_dtype is None or \
            node_name_to_target_dtype[node.name]["input_activation_dtype"] == input_activation_dtype
    elif is_weight:
        weight_dtype = dtype_config.get("weight_dtype", None)
        return weight_dtype is None or node_name_to_target_dtype[node.name]["weight_dtype"] == weight_dtype
    else:  # bias
        bias_dtype = dtype_config.get("bias_dtype", None)
        return bias_dtype is None or node_name_to_target_dtype[node.name]["bias_dtype"] == bias_dtype
