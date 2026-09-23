@symbolic_helper.parse_args("v", "is", "is", "is", "is", "i")
def max_pool2d(
    g: jit_utils.GraphContext,
    input,
    kernel_size,
    stride,
    padding,
    dilation,
    ceil_mode,
):
    if input not in symbolic_helper._quantized_ops:
        return opset9.max_pool2d(  # type: ignore[attr-defined]
            g, input, kernel_size, stride, padding, dilation, ceil_mode
        )
    kwargs = {
        "strides_i": stride,
        "pads_i": padding + padding,
        "kernel_i": kernel_size[0],
        "order_s": "NHWC",
        "Y_scale_f": symbolic_helper._node_get(input.node(), "Y_scale"),
        "Y_zero_point_i": symbolic_helper._node_get(input.node(), "Y_zero_point"),
    }
    input = nchw2nhwc(g, input)
    output = g.op("_caffe2::Int8MaxPool", input, **kwargs)
    output = nhwc2nchw(g, output)
    symbolic_helper._quantized_ops.add(output)
    return output
