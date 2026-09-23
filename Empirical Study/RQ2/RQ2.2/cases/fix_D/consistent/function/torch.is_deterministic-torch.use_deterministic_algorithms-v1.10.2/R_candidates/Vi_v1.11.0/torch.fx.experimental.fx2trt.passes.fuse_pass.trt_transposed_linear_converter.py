    @tensorrt_converter(trt_transposed_linear)
    def trt_transposed_linear_converter(network, target, args, kwargs, name):
        input, weight, bias = args

        weight = get_trt_tensor(network, weight.t(), f"{name}_weight")
        bias = get_trt_tensor(network, bias.reshape(1, -1), f"{name}_bias")

        input, weight = broadcast(network, input, weight, f"{input.name}_broadcast", f"{weight.name}_broadcast")
        layer = network.add_matrix_multiply(
            input,
            trt.MatrixOperation.TRANSPOSE,
            weight,
            trt.MatrixOperation.NONE,
        )
        set_layer_name(layer, target, f"{name}_mm")
        return add_binary_elementwise_layer(
            network, layer.get_output(0), bias, trt.ElementWiseOperation.SUM, target, f"{name}_add"
        )
