@tensorrt_converter(acc_ops.sigmoid)
def acc_ops_sigmoid(network, target, args, kwargs, name):
    input_val = kwargs["input"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(
            f"Sigmoid received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    layer = network.add_activation(input=input_val, type=trt.ActivationType.SIGMOID)
    layer.name = name
    return layer.get_output(0)
