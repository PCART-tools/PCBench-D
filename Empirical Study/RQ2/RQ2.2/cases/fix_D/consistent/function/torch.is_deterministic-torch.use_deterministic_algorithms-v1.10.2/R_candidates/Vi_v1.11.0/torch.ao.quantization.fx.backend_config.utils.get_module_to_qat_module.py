def get_module_to_qat_module(
        backend_config_dict: Dict[str, Any]) -> Dict[Callable, Callable]:
    module_to_qat_module: Dict[Callable, Callable] = dict()
    for config in backend_config_dict.get("configs", []):
        if "pattern" in config and "qat_module" in config:
            pattern = config["pattern"]
            qat_module = config["qat_module"]
            module_to_qat_module[pattern] = qat_module

    return module_to_qat_module
