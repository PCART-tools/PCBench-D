def common_maxpool(network, mod, dimension, input_val, layer_name):
    kernel_size = extend_attr_to_tuple(mod, "kernel_size", dimension)
    stride = extend_attr_to_tuple(mod, "stride", dimension)
    padding = extend_attr_to_tuple(mod, "padding", dimension)

    layer = network.add_pooling(
        input=input_val, type=trt.PoolingType.MAX, window_size=kernel_size)

    layer.stride = stride
    layer.padding = padding
    layer.name = layer_name

    if mod.ceil_mode:
        layer.padding_mode = trt.PaddingMode.EXPLICIT_ROUND_UP

    if input_val.dynamic_range:
        mark_as_int8_layer(layer, input_val.dynamic_range)

    return layer.get_output(0)
