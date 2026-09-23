def save_state(
    observed: GraphModule,
    qconfig_map: Dict[str, QConfigAny],
    node_name_to_scope: Dict[str, Tuple[str, type]],
    patterns: Dict[Pattern, QuantizeHandler],
    prepare_custom_config_dict: Dict[str, Any],
    equalization_qconfig_map: Dict[str, Any],
    qconfig_dict: Dict[str, Dict[Any, Any]],
    is_qat: bool,
    observed_node_names: Set[str],
) -> None:
    observed._patterns = patterns  # type: ignore[assignment]
    observed._qconfig_map = qconfig_map  # type: ignore[assignment]
    observed._prepare_custom_config_dict = \
        prepare_custom_config_dict  # type: ignore[assignment]
    observed._node_name_to_scope = node_name_to_scope  # type: ignore[assignment]
    observed._equalization_qconfig_map = equalization_qconfig_map  # type: ignore[assignment]
    observed._qconfig_dict = qconfig_dict  # type: ignore[assignment]
    observed._is_qat = is_qat  # type: ignore[assignment]
    observed._observed_node_names = observed_node_names  # type: ignore[assignment]
