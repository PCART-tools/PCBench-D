def is_output_dtype_supported_by_backend(
    node: Node,
    node_name_to_target_dtype: Dict[str, Dict[str, Optional[torch.dtype]]],
    dtype_config: Dict[str, torch.dtype],
) -> bool:
    """ Check if the configured qconfig for the output
    is supported by the backend or not
    """
    output_dtype = dtype_config.get("output_dtype", None)
    return output_dtype is None or \
        output_dtype == node_name_to_target_dtype[node.name]["output_activation_dtype"]
