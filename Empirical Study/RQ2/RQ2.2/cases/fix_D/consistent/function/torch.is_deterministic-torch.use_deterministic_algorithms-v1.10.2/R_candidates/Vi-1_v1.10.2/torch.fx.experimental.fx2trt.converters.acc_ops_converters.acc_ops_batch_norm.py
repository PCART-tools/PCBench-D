@tensorrt_converter(acc_ops.batch_norm)
def acc_ops_batch_norm(network, target, args, kwargs, name):
    input_val = kwargs["input"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(
            f"BatchNorm2d received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    if has_dynamic_shape(input_val.shape):
        assert input_val.shape[1] != -1, "Channel dim can't be dynamic for batch norm."

    scale = to_numpy(kwargs["weight"]) / np.sqrt(
        to_numpy(kwargs["running_var"]) + kwargs["eps"]
    )
    bias = (
        to_numpy(kwargs["bias"])
        - to_numpy(kwargs["running_mean"]) * scale
    )
    power = np.ones_like(scale)

    layer = network.add_scale(input_val, trt.ScaleMode.CHANNEL, bias, scale, power)
    layer.name = name

    return layer.get_output(0)
