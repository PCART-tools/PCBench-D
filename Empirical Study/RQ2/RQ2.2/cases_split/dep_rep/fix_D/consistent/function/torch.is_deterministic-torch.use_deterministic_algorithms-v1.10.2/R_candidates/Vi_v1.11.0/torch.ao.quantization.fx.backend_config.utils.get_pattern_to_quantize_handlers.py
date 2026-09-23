def get_pattern_to_quantize_handlers(
        backend_config_dict: Dict[str, Any]) -> Dict[Pattern, QuantizerCls]:
    """
    Note: Quantize handler is just a holder for some check methods like
    (should_insert_observer_for_output), maybe this can be a enum as well,
    we can refactor this after we convert the path for fbgemm/qnnpack fully to the
    new path, this is not exposed to backend developers
    """
    pattern_to_quantize_handlers = dict()
    for config in backend_config_dict.get("configs", []):
        pattern = config["pattern"]
        observation_type = config["observation_type"]
        dtype_configs = config["dtype_configs"]
        pattern_to_quantize_handlers[pattern] = \
            get_quantize_handler_cls(observation_type, dtype_configs)

    return pattern_to_quantize_handlers
