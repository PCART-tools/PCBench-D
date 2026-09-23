def common_batchnorm(network, mod, input_val, layer_name, is_quantized):
    scale = to_numpy(mod.weight) / np.sqrt(
        to_numpy(mod.running_var) + mod.eps
    )
    bias = (
        to_numpy(mod.bias)
        - to_numpy(mod.running_mean) * scale
    )
    power = np.ones_like(scale)

    layer = network.add_scale(input_val, trt.ScaleMode.CHANNEL, bias, scale, power)
    layer.name = layer_name

    if is_quantized:
        mark_as_int8_layer(layer, get_dyn_range(mod.scale, mod.zero_point, torch.quint8))

    return layer.get_output(0)
