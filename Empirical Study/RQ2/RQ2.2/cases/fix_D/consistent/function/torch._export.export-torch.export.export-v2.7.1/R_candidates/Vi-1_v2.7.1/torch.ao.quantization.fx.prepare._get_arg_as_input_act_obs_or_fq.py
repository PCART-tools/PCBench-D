def _get_arg_as_input_act_obs_or_fq(
    arg: Node,
    node: Node,
    named_modules: dict[str, torch.nn.Module],
    obs_or_fq_map: dict[EdgeOrNode, ObserverOrFakeQuantize],
    is_qat: bool,
) -> Optional[ObserverOrFakeQuantize]:
    """Get the observer or fake quant constructor for the Argument `arg`, as input
    to Node `node`
    """
    assert isinstance(arg, Node)
    # "input_qspec_map" is the more general design we'll use for pt2e path
    # it is a map from input argument node to observer or fake quant constructor, for example
    # for the following graph:
    # x -> conv -> output
    #
    # we may annotate conv node like the following:
    # conv.meta[...] = QuantizationAnnotation("input_qspec_map": {x: MinMaxObserver.with_args(dtype=torch.qint8)}, ...)
    #
    if "quantization_annotation" in node.meta:
        input_qspec_map = node.meta["quantization_annotation"].input_qspec_map
        input_arg_qspec = _get_qspec_for_arg(arg, input_qspec_map, named_modules)
        if input_arg_qspec is None:
            input_arg_obs_or_fq = _DEFAULT_FP32_OBS_OR_FQ_CTR()
        else:
            input_arg_obs_or_fq = _create_obs_or_fq_from_qspec(
                input_arg_qspec, obs_or_fq_map, is_qat
            )
        return input_arg_obs_or_fq

    # we can remove the following path in the future if fx graph mode quantization is
    # no longer used
    is_weight = node_arg_is_weight(node, arg)
    is_bias = node_arg_is_bias(node, arg)
    is_activation = not is_weight and not is_bias
    obs_or_fq_ctr = None
    if is_activation:
        obs_or_fq_ctr = node.meta["target_dtype_info"].get(
            "input_act_obs_or_fq_ctr", _DEFAULT_FP32_OBS_OR_FQ_CTR
        )
    elif is_weight:
        if node.target not in NON_QUANTIZABLE_WEIGHT_OPS:
            obs_or_fq_ctr = node.meta["target_dtype_info"].get(
                "weight_obs_or_fq_ctr", _DEFAULT_FP32_OBS_OR_FQ_CTR
            )
    else:
        obs_or_fq_ctr = node.meta["target_dtype_info"].get(
            "bias_obs_or_fq_ctr", _DEFAULT_FP32_OBS_OR_FQ_CTR
        )
    return obs_or_fq_ctr() if obs_or_fq_ctr else None
