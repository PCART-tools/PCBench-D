@tensorrt_converter(acc_ops.clamp)
def acc_ops_clamp(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    min_val = kwargs["min"]
    max_val = kwargs["max"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(
            f"Clamp received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    if min_val is not None:
        clamp_min_layer = add_clamp(
            network, input_val, min_val, trt.ElementWiseOperation.MAX
        )
        clamp_min_layer.name = f"{name}_clamp_min"
        input_val = clamp_min_layer.get_output(0)
    if max_val is not None:
        clamp_max_layer = add_clamp(
            network, input_val, max_val, trt.ElementWiseOperation.MIN
        )
        clamp_max_layer.name = f"{name}_clamp_max"
        input_val = clamp_max_layer.get_output(0)

    return input_val
