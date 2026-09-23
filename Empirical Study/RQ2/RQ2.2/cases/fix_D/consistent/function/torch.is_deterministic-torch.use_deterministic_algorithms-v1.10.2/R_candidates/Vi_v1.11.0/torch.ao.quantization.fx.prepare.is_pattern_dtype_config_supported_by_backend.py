def is_pattern_dtype_config_supported_by_backend(
    pattern: Optional[Pattern],
    matched_nodes: Optional[List[Node]],
    node_name_to_target_dtype: Dict[str, Dict[str, Optional[torch.dtype]]],
    backend_config_dict: Optional[Dict[str, Any]]
) -> bool:
    """ Check is the dtype configuration of a pattern is supported by
    the backend or not
    """
    if backend_config_dict is None or pattern is None:
        return True
    assert matched_nodes is not None and len(matched_nodes) >= 1
    pattern_to_dtype_configs = get_pattern_to_dtype_configs(backend_config_dict)
    dtype_configs: List[Dict[str, torch.dtype]] = pattern_to_dtype_configs.get(pattern, [])

    # TODO: this only checks one input and one output, need to generalize to multiple
    # inputs/output
    input_node = matched_nodes[-1]
    output_node = matched_nodes[0]
    for dtype_config in dtype_configs:
        # check if arg dtype are supported
        supported = True
        for arg in input_node.args:
            supported = supported and \
                is_input_arg_dtype_supported_by_backend(
                    arg, input_node, node_name_to_target_dtype, dtype_config)
        for k, arg in input_node.kwargs.items():
            supported = supported and \
                is_input_arg_dtype_supported_by_backend(
                    arg, input_node, node_name_to_target_dtype, dtype_config)
        # check if output dtype is supported
        supported = supported and is_output_dtype_supported_by_backend(
            output_node, node_name_to_target_dtype, dtype_config)
        if supported:
            return True
    return False
