def _get_linear_configs() -> list[BackendPatternConfig]:
    """
    Return all configs related to linear modules and ops.
    """
    observation_type = ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT
    dtype_configs = [
        qnnpack_weighted_op_qint8_symmetric_dtype_config,
        executorch_weighted_op_int8_dtype_config,
        executorch_default_dynamic_quint8_dtype_config,
        executorch_default_dynamic_qint8_dtype_config,
        executorch_default_dynamic_float16_dtype_config,
    ]
    linear_configs: list[BackendPatternConfig] = []
    # linear module
    linear_configs.append(
        BackendPatternConfig(torch.nn.Linear)
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        .set_root_module(torch.nn.Linear)
        .set_reference_quantized_module(nnqr.Linear)
        .set_qat_module(nnqat.Linear)
    )
    # linear qat module
    linear_configs.append(
        BackendPatternConfig(nnqat.Linear)
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        .set_root_module(torch.nn.Linear)
        .set_reference_quantized_module(nnqr.Linear)
    )
    # functional linear
    linear_configs.append(
        BackendPatternConfig(torch.nn.functional.linear)
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        ._set_input_type_to_index({"weight": 1, "bias": 2})
    )
    return linear_configs
