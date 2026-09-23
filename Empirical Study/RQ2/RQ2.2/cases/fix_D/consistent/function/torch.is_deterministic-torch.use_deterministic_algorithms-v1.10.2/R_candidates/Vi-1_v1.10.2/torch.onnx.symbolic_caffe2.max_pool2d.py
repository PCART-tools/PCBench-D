@parse_args("v", "is", "is", "is", "is", "i")
def max_pool2d(g, input, kernel_size, stride, padding, dilation, ceil_mode):
    if input not in sym_help._quantized_ops:
        from torch.onnx.symbolic_opset9 import max_pool2d
        return max_pool2d(g, input, kernel_size, stride, padding, dilation, ceil_mode)
    kwargs = {
        "strides_i": stride,
        "pads_i": padding + padding,
        "kernel_i": kernel_size[0],
        "order_s": "NHWC",
        "Y_scale_f": input.node()["Y_scale"],
        "Y_zero_point_i": input.node()["Y_zero_point"],
    }
    input = nchw2nhwc(g, input)
    output = g.op("_caffe2::Int8MaxPool", input, **kwargs)
    output = nhwc2nchw(g, output)
    sym_help._quantized_ops.add(output)
    return output
