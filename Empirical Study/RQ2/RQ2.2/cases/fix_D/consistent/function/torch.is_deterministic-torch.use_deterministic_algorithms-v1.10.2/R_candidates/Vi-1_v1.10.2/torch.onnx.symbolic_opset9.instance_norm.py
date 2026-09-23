@parse_args("v", "v", "v", "v", "v", "i", "f", "f", "i")
def instance_norm(g, input, weight, bias, running_mean, running_var, use_input_stats, momentum, eps, cudnn_enabled):
    if running_mean is None or sym_help._is_none(running_mean) or running_var is None or sym_help._is_none(running_var):
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
        return g.op("InstanceNormalization", input, weight, bias, epsilon_f=eps)
    else:
        # Now if track_running_stats is set to True it would get the same result with batchnorm. The PyTorch internal
        # implementation of instance_norm may have a problem with running_mean and running_var repeat, will open a github issue.
        return batch_norm(g, input, weight, bias, running_mean, running_var, use_input_stats, momentum, eps, cudnn_enabled)
