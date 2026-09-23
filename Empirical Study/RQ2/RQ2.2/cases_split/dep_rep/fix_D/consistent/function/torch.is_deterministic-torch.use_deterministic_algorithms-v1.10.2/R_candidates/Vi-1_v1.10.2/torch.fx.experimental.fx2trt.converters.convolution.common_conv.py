def common_conv(network, mod, dimension, input_val, layer_name, is_quantized):
    if mod.padding_mode != "zeros":
        raise RuntimeError(f"Only support padding mode: zeros, got {mod.padding_mode}.")

    kernel_size = extend_attr_to_tuple(mod, "kernel_size", dimension)
    stride = extend_attr_to_tuple(mod, "stride", dimension)
    padding = extend_attr_to_tuple(mod, "padding", dimension)
    dilation = extend_attr_to_tuple(mod, "dilation", dimension)

    kernel = to_numpy(mod.weight() if is_quantized else mod.weight)
    bias = to_numpy(mod.bias() if is_quantized else mod.bias)

    layer = network.add_convolution(
        input=input_val,
        num_output_maps=mod.out_channels,
        kernel_shape=kernel_size,
        kernel=kernel,
        bias=bias,
    )
    layer.name = layer_name
    layer.stride = stride
    layer.padding = padding
    layer.dilation = dilation
    layer.num_groups = mod.groups

    if is_quantized:
        # Assume the dtype of activation is torch.quint8
        mark_as_int8_layer(layer, get_dyn_range(mod.scale, mod.zero_point, torch.quint8))

    return layer.get_output(0)
