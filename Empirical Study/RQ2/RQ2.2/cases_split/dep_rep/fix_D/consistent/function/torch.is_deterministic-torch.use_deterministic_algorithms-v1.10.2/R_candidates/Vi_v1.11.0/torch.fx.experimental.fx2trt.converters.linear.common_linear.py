def common_linear(network, mod, input_val, layer_name, is_quantized):
    """
    TensorRT fully connected layer implicitly flatten last three dimensions at
    the start and implicitly reshape the result to (K, 1, 1) at the end.

    e.g. If input is (N, C, H, W), first it gets flatten to (N, C*H*W). Then after
    going through fully connected operation, it becomes (N, K). Before sending it
    out, it gets reshaped into (N, K, 1, 1) and this is the final output.

    TODO: We can optimize this to get rid of unneccesary transformation.
    """
    # reshape the input to (*, X, 1, 1)
    layer = network.add_shuffle(input_val)
    layer.reshape_dims = tuple(input_val.shape) + (1, 1)
    layer.name = f"{layer_name}_pre_shuffle"

    if is_quantized:
        mark_as_int8_layer(layer, input_val.dynamic_range)

    kernel = to_numpy(mod.weight if not is_quantized else mod.weight())
    bias = to_numpy(mod.bias if not is_quantized else mod.bias())

    # add fully connected
    layer = network.add_fully_connected(
        input=layer.get_output(0),
        num_outputs=mod.out_features,
        kernel=kernel,
        bias=bias
    )
    layer.name = f"{layer_name}_linear"

    if is_quantized:
        dyn_range = get_dyn_range(mod.scale, mod.zero_point, torch.quint8)
        mark_as_int8_layer(layer, dyn_range)

    # reshape the output from (*, K, 1, 1) to (*, K)
    layer = network.add_shuffle(layer.get_output(0))
    layer.reshape_dims = tuple(input_val.shape[:-1]) + (mod.out_features,)
    layer.name = f"{layer_name}_post_shuffle"

    if is_quantized:
        mark_as_int8_layer(layer, dyn_range)

    return layer.get_output(0)
