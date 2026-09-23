@tensorrt_converter(acc_ops.max_pool2d)
def acc_ops_max_pool2d(network, target, args, kwargs, name):
    input_val = kwargs["input"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(
            f"MaxPool2d received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    kernel_size = process_attr(kwargs["kernel_size"], 2)
    stride = process_attr(kwargs["stride"], 2)
    padding = process_attr(kwargs["padding"], 2)
    dilation = process_attr(kwargs["dilation"], 2)
    ceil_mode = kwargs["ceil_mode"]

    if dilation != (1, 1):
        raise RuntimeError(
            f"Only support dilation=(1, 1) for maxpool, but got {dilation}"
        )

    layer = network.add_pooling(
        input=input_val, type=trt.PoolingType.MAX, window_size=kernel_size
    )
    layer.stride = stride
    layer.padding = padding
    layer.name = name

    if ceil_mode:
        layer.padding_mode = trt.PaddingMode.EXPLICIT_ROUND_UP

    return layer.get_output(0)
