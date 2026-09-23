def _get_supported_symmetric_config_and_operators() -> list[OperatorConfig]:
    supported_config_and_operators: list[OperatorConfig] = []
    for quantization_config in [
        get_symmetric_quantization_config(),
        get_symmetric_quantization_config(is_qat=True),
        get_symmetric_quantization_config(is_per_channel=True),
        get_symmetric_quantization_config(is_per_channel=True, is_qat=True),
    ]:
        ops = _supported_symmetric_quantized_operators()
        supported_config_and_operators.extend(
            OperatorConfig(quantization_config, pattern_list)
            for pattern_list in ops.values()
        )
    return copy.deepcopy(supported_config_and_operators)
