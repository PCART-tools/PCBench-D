def add_unary_layer(network, input_val, operation_type, name):
    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(
            f"{operation_type} received input {input_val} that is not part "
            "of the TensorRT region!"
        )
    layer = network.add_unary(input_val, operation_type)
    layer.name = name
    return layer.get_output(0)
