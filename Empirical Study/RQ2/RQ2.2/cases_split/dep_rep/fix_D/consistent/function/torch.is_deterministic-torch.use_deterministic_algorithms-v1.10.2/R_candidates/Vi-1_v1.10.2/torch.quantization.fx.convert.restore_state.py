def restore_state(
        observed: GraphModule
) -> Tuple[Dict[Pattern, QuantizeHandler], Dict[str, Tuple[str, type]], Dict[str, Any]]:
    assert is_observed_module(observed), \
        'incoming model must be produced by prepare_fx'
    prepare_custom_config_dict: Dict[str, Any] = \
        observed._prepare_custom_config_dict  # type: ignore[assignment]
    node_name_to_scope: Dict[str, Tuple[str, type]] = observed._node_name_to_scope  # type: ignore[assignment]
    patterns: Dict[Pattern, QuantizeHandler] = observed._patterns  # type: ignore[assignment]
    return patterns, node_name_to_scope, prepare_custom_config_dict
