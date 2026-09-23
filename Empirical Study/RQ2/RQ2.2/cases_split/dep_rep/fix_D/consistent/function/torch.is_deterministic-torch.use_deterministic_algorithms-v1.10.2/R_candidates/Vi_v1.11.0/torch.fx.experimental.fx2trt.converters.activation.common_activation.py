def common_activation(network, mod, input_val, activation_type, activation_dyn_range_fn, layer_name):
    layer = network.add_activation(
        input=input_val, type=activation_type)
    layer.name = layer_name

    if input_val.dynamic_range:
        dyn_range = activation_dyn_range_fn(input_val.dynamic_range)
        mark_as_int8_layer(layer, dyn_range)

    return layer.get_output(0)
