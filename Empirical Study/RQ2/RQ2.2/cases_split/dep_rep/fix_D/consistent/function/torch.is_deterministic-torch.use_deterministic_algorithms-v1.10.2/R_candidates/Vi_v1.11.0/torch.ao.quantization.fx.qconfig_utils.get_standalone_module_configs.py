def get_standalone_module_configs(
        module_name: str,
        module_type: Callable,
        custom_config_dict: Dict[str, Any]):
    standalone_module_name_configs = \
        custom_config_dict.get("standalone_module_name", [])
    standalone_module_class_configs = \
        custom_config_dict.get("standalone_module_class", [])
    class_config_map = {x[0]: (x[1], x[2], x[3]) for x in standalone_module_class_configs}
    name_config_map = {x[0]: (x[1], x[2], x[3]) for x in standalone_module_name_configs}
    config = class_config_map.get(module_type, (None, None, None))
    # name config has precedence over type config
    config = name_config_map.get(module_name, config)
    return config
