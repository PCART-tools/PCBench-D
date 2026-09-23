def _get_quantized_conv_bn_example_inputs_kwargs(
    is_per_channel: bool,
    has_bias: bool,
    bias_is_quantized: bool,
    is_cuda: bool,
) -> dict[str, Any]:
    """
    Optional example inputs for quantized and folded conv-bn patterns
    used in convert, expressed as kwargs.
    """
    kwargs = {}
    # Per tensor quantization uses literals to represent scale and zero
    # point, so there is no need to include them here as kwargs
    if is_per_channel:
        kwargs["weight_scale"] = torch.tensor([1], dtype=torch.float)
        kwargs["weight_zero_point"] = torch.tensor([0], dtype=torch.int)
        if has_bias and bias_is_quantized:
            kwargs["bias_scale"] = torch.tensor([1], dtype=torch.float)
            kwargs["bias_zero_point"] = torch.tensor([0], dtype=torch.int)
    if has_bias:
        kwargs["conv_bias"] = torch.randn(1)
    if is_cuda:
        for k, v in kwargs.items():
            if isinstance(v, torch.Tensor):
                kwargs[k] = v.cuda()
    return kwargs
