def get_fuser_method_mapping(
        backend_config_dict: Dict[str, Any]) -> Dict[Pattern, Union[nn.Sequential, Callable]]:
    fuser_method_mapping : Dict[Pattern, Union[nn.Sequential, Callable]] = dict()
    for config in backend_config_dict.get("configs", []):
        if "fuser_method" in config:
            pattern = config["pattern"]
            fuser_method = config["fuser_method"]
            fuser_method_mapping[pattern] = fuser_method

    return fuser_method_mapping
