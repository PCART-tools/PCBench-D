def common_conv_relu(network, mod, dimension, input_val, layer_name, is_quantized):
    conv_output = common_conv(
        network,
        mod,
        dimension=2,
        input_val=input_val,
        layer_name=f"{layer_name}_conv",
        is_quantized=is_quantized,
    )

    layer = network.add_activation(
        input=conv_output, type=trt.ActivationType.RELU)
    layer.name = f"{layer_name}_relu"

    if is_quantized:
        mark_as_int8_layer(layer, conv_output.dynamic_range)

    return layer.get_output(0)
