@parse_args("v", "v", "v", "v", "v", "i", "f", "f", "i")
def instance_norm(g, input, weight, bias, running_mean, running_var, use_input_stats, momentum, eps, cudnn_enabled):
    sym_help.check_training_mode(use_input_stats, "instance_norm")
    channel_size = sym_help._get_tensor_dim_size(input, 1)
    if weight is None or sym_help._is_none(weight):
        if channel_size is None:
            raise RuntimeError("Unsupported: ONNX export of instance_norm for unknown "
                               "channel size.")
        weight_value = torch.tensor([1.] * channel_size).type(
            "torch." + input.type().scalarType() + "Tensor")
        weight = g.op("Constant", value_t=weight_value)
    if bias is None or sym_help._is_none(bias):
        if channel_size is None:
            raise RuntimeError("Unsupported: ONNX export of instance_norm for unknown "
                               "channel size.")
        bias_value = torch.tensor([0.] * channel_size).type(
            "torch." + input.type().scalarType() + "Tensor")
        bias = g.op("Constant", value_t=bias_value)
    if running_mean is None or sym_help._is_none(running_mean) or running_var is None or sym_help._is_none(running_var):
        return g.op("InstanceNormalization", input, weight, bias, epsilon_f=eps)
    else:
        input_size = sym_help._get_tensor_sizes(input)
        # If input shape is [N, C, H, W], reshape to [1, N * C, H, W] and call batch_norm.
        # For more information instance_norm():
        # https://github.com/pytorch/pytorch/blob/master/aten/src/ATen/native/Normalization.cpp#L542
        input_size_reshape = input_size.copy()
        n = input_size[0]
        if n is None:
            raise RuntimeError("Unsupported: ONNX export of instance_norm training for unknown "
                               "batch size.")
        c = input_size[1]
        input_size_reshape[0] = 1
        input_size_reshape[1] = n * c
        weight_ = repeat(g, weight, g.op("Constant", value_t=torch.tensor([n], dtype=torch.int64)))
        bias_ = repeat(g, bias, g.op("Constant", value_t=torch.tensor([n], dtype=torch.int64)))
        running_mean_ = repeat(g, running_mean, g.op("Constant", value_t=torch.tensor([n], dtype=torch.int64)))
        running_var_ = repeat(g, running_var, g.op("Constant", value_t=torch.tensor([n], dtype=torch.int64)))
        input_reshaped = g.op("Reshape", input, g.op("Constant", value_t=torch.LongTensor(input_size_reshape)))
        out = batch_norm(g, input_reshaped, weight_, bias_, running_mean_, running_var_, use_input_stats,
                         momentum, eps, cudnn_enabled)
        return view(g, out, g.op("Constant", value_t=torch.tensor(input_size)))
