def get_pattern_to_input_type_to_index(
        backend_config_dict: Dict[str, Any]) -> Dict[Pattern, Dict[str, int]]:
    pattern_to_input_type_to_index: Dict[Pattern, Dict[str, int]] = dict()
    for config in backend_config_dict.get("configs", []):
        pattern = config["pattern"]
        input_type_to_index = config.get("input_type_to_index", {})
        pattern_to_input_type_to_index[pattern] = input_type_to_index
    return pattern_to_input_type_to_index
