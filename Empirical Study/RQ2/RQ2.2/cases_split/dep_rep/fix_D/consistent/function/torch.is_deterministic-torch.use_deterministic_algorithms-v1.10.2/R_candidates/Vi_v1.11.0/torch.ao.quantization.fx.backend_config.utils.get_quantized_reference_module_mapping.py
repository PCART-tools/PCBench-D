def get_quantized_reference_module_mapping(
        backend_config_dict: Dict[str, Any]) -> Dict[Callable, Callable]:
    mapping: Dict[Callable, Callable] = dict()
    for config in backend_config_dict.get("configs", []):
        if "root_module" in config and "reference_quantized_module_for_root" in config:
            mapping[config["root_module"]] = config["reference_quantized_module_for_root"]
    return mapping
