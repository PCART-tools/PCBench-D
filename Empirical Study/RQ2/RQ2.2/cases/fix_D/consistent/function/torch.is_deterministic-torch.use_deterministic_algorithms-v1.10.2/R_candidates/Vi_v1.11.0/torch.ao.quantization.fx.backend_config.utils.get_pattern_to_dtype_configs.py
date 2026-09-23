def get_pattern_to_dtype_configs(
        backend_config_dict: Dict[str, Any]) -> Dict[Pattern, List[Dict[str, torch.dtype]]]:
    pattern_to_dtype_configs: Dict[Pattern, List[Dict[str, torch.dtype]]] = dict()
    for config in backend_config_dict.get("configs", []):
        pattern = config["pattern"]
        dtype_configs = config["dtype_configs"]
        pattern_to_dtype_configs[pattern] = dtype_configs
    return pattern_to_dtype_configs
