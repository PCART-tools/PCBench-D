@parse_args("v", "i", "v", "v", "f", "i")
def group_norm(g, input, num_groups, weight, bias, eps, cudnn_enabled):
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        return g.op("ATen", input, weight, bias, num_groups_i=num_groups,
                    eps_f=eps, cudnn_enabled_i=cudnn_enabled, operator_s="group_norm")

    channel_size = sym_help._get_tensor_dim_size(input, 1)
    if channel_size is not None:
        assert channel_size % num_groups == 0
    input_rank = sym_help._get_tensor_rank(input)
    if input_rank is None:
        return _unimplemented("group_norm", "unknown input rank")
    # 0 in the shape list keeps dimension value unchanged.
    shape = [0, num_groups, -1]
    input_reshaped = sym_help._reshape_helper(g, input,
                                              g.op("Constant", value_t=torch.LongTensor(shape)))

    # C is always divisible by num_groups
    # Due to shape difference. we need to apply weight and bias after
    # instance norm computation and reshape
    weight_ = g.op("Constant", value_t=torch.tensor([1.] * num_groups).type(
        "torch." + input.type().scalarType() + "Tensor"))
    bias_ = g.op("Constant", value_t=torch.tensor([0.] * num_groups).type(
        "torch." + input.type().scalarType() + "Tensor"))

    norm_reshaped = g.op("InstanceNormalization", input_reshaped, weight_, bias_, epsilon_f=eps)
    norm = sym_help._reshape_helper(g, norm_reshaped, g.op("Shape", input))

    if weight is None or weight.node().mustBeNone():
        weight_value = torch.tensor([1.]).type(
            "torch." + input.type().scalarType() + "Tensor")
        weight = g.op("Constant", value_t=weight_value)
    if bias is None or bias.node().mustBeNone():
        bias_value = torch.tensor([0.]).type(
            "torch." + input.type().scalarType() + "Tensor")
        bias = g.op("Constant", value_t=bias_value)

    # Norm has shape [N, C, *] so we reshape weight and bias to [C, *]
    axes = list(range(1, input_rank - 1))
    return add(g, mul(g, norm, sym_help._unsqueeze_helper(g, weight, axes)), sym_help._unsqueeze_helper(g, bias, axes))
