@tensorrt_converter(acc_ops.adaptive_avg_pool2d)
def acc_ops_adaptive_avg_pool2d(network, target, args, kwargs, name):
    input_val = kwargs["input"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(
            f"AdaptiveAvgPool2d received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    assert (
        input_val.shape[-1] != -1 and input_val.shape[-1] != -1
    ), "AdaptiveAvgPool2d currently doesn't support dynamic shapes for last two dims."
    output_size = kwargs["output_size"]

    for input_dim, output_dim in zip(input_val.shape[-2:], output_size):
        if input_dim % output_dim != 0:
            raise RuntimeError(
                "For AdaptiveAvgPool, input dim has to be integer multiple of output dim."
                f"Got input dim {input_dim}, output dim {output_dim}"
            )

    stride = (
        input_val.shape[-2] // output_size[0],
        input_val.shape[-1] // output_size[1],
    )
    kernel_size = (
        input_val.shape[-2] - (output_size[0] - 1) * stride[0],
        input_val.shape[-1] - (output_size[1] - 1) * stride[1],
    )
    layer = network.add_pooling(
        input=input_val, type=trt.PoolingType.AVERAGE, window_size=kernel_size
    )
    layer.stride = stride
    layer.name = name

    return layer.get_output(0)
