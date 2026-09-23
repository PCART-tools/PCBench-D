@parse_args("v", "is", "is", "is", "i", "i", "none")
def avg_pool2d(g, input, kernel_size, stride, padding, ceil_mode, count_include_pad, divisor_override=None):
    if input not in sym_help._quantized_ops:
        from torch.onnx.symbolic_opset9 import avg_pool2d
        return avg_pool2d(g, input, kernel_size, stride, padding, ceil_mode, count_include_pad, divisor_override)
    kwargs = {
        "strides_i": stride,
        "pads_i": padding + padding,
        "kernel_i": kernel_size[0],
        "order_s": "NHWC",
        "Y_scale_f": input.node()["Y_scale"],
        "Y_zero_point_i": input.node()["Y_zero_point"],
    }
    input = nchw2nhwc(g, input)
    output = g.op("_caffe2::Int8AveragePool", input, **kwargs)
    output = nhwc2nchw(g, output)
    sym_help._quantized_ops.add(output)
    return output
