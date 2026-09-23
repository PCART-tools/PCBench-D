def _get_conv_configs() -> list[BackendPatternConfig]:
    """
    Return all configs related to conv modules and ops.
    """
    observation_type = ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT
    dtype_configs = [
        qnnpack_weighted_op_qint8_symmetric_dtype_config,
        executorch_weighted_op_int8_dtype_config,
    ]
    conv_configs = []
    for convs in [_Conv2dMetadata]:
        # (1) Single conv modules/functions
        # -----------------------------------
        # conv module
        conv_configs.append(
            BackendPatternConfig(convs.root)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
            .set_qat_module(convs.qat)
        )
        # conv qat module
        conv_configs.append(
            BackendPatternConfig(convs.qat)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
        )
        # functional conv
        conv_configs.append(
            BackendPatternConfig(convs.func)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            ._set_input_type_to_index({"weight": 1, "bias": 2})
        )

        # (2) Conv + relu
        # -----------------------------------
        # conv module + relu module
        conv_configs.append(
            BackendPatternConfig((convs.root, nn.ReLU))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_fuser_method(_sequential_wrapper2(convs.fused_conv_relu))
            .set_fused_module(convs.fused_conv_relu)
        )
        # conv module + functional relu
        conv_configs.append(
            BackendPatternConfig((convs.root, F.relu))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_fuser_method(_sequential_wrapper2(convs.fused_conv_relu))
            .set_fused_module(convs.fused_conv_relu)
        )
        # fused conv relu module
        conv_configs.append(
            BackendPatternConfig(convs.fused_conv_relu)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
            .set_qat_module(convs.relu_qat)
        )
        # conv relu, qat fused module
        conv_configs.append(
            BackendPatternConfig(convs.relu_qat)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
        )
        # functional conv + relu module
        conv_configs.append(
            BackendPatternConfig((convs.func, nn.ReLU))
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
        )
        # functional conv + functional relu
        conv_configs.append(
            BackendPatternConfig((convs.func, F.relu))
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
        )
        # fused conv relu
        conv_configs.append(
            BackendPatternConfig(convs.fused_conv_relu)
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_qat_module(convs.relu_qat)
        )

        conv_configs.append(
            BackendPatternConfig(convs.relu_qat)
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
        )

        # (3) Conv + batchnorm (+ relu)
        # -------------------------------
        # conv + batchnorm (+ relu)
        conv_configs.append(
            BackendPatternConfig((convs.root, convs.bn))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_fuser_method(fuse_conv_bn)
            .set_fused_module(convs.fused_conv_bn)
        )
        # conv + bn + relu module fusion
        conv_configs.append(
            BackendPatternConfig((convs.root, convs.bn, nn.ReLU))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_fuser_method(fuse_conv_bn_relu)
            .set_fused_module(convs.fused_conv_bn_relu)
        )
        # conv + bn + relu functional fusion
        conv_configs.append(
            BackendPatternConfig((convs.root, convs.bn, F.relu))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_root_module(convs.root)
            .set_fuser_method(fuse_conv_bn_relu)
            .set_fused_module(convs.fused_conv_bn_relu)
        )
        # TODO: we can add fusion for torch.relu as well
        # 3.2 conv + bn (+ relu) fused module configs
        # fused conv bn
        conv_configs.append(
            BackendPatternConfig(convs.fused_conv_bn)
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_qat_module(convs.bn_qat)
        )

        # fused conv bn relu
        conv_configs.append(
            BackendPatternConfig(convs.fused_conv_bn_relu)
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_qat_module(convs.bn_relu_qat)
        )

        # conv bn, qat fused module
        conv_configs.append(
            BackendPatternConfig(convs.bn_qat)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
        )
        # conv bn relu, qat fused module
        conv_configs.append(
            BackendPatternConfig(convs.bn_relu_qat)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
        )
    return conv_configs
