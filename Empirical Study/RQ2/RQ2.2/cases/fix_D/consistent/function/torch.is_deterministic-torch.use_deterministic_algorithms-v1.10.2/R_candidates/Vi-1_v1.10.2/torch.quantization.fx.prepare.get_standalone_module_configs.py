def get_standalone_module_configs(
    node: Node,
    modules: Dict[str, torch.nn.Module],
    prepare_custom_config_dict: Dict[str, Any],
    qconfig: QConfigAny,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Returns the standalone module qconfig_dict and prepare_config_dict
    for `node`, assuming that the module pointed to by `node` is
    a standalone modules.
    """
    standalone_module = modules[node.target]  # type: ignore[index]
    standalone_module_name_configs = \
        prepare_custom_config_dict.get("standalone_module_name", [])
    standalone_module_class_configs = \
        prepare_custom_config_dict.get("standalone_module_class", [])
    class_config_map = {x[0]: (x[1], x[2]) for x in standalone_module_class_configs}
    name_config_map = {x[0]: (x[1], x[2]) for x in standalone_module_name_configs}
    config = class_config_map.get(type(standalone_module), (None, None))
    config = name_config_map.get(node.target, config)
    sm_qconfig_dict = {"": qconfig} if config[0] is None else config[0]
    sm_prepare_config_dict = {} if config[1] is None else config[1]
    return sm_qconfig_dict, sm_prepare_config_dict
