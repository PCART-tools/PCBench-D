@parse_args("v", "v", "v", "is", "is", "is", "i", "f", "i")
def conv2d_relu(g, input, weight, bias, stride, padding, dilation, groups, scale, zero_point):
    kernel_size = weight.node()["shape"][1:3]
    kwargs = {
        "strides_i": stride,
        "pads_i": padding + padding,
        "dilations_i": dilation,
        "group_i": groups,
        "kernels_i": kernel_size,
        "order_s": "NHWC",
        "Y_scale_f": scale,
        "Y_zero_point_i": zero_point,
    }
    output = g.op("_caffe2::Int8ConvRelu", input, weight, bias, **kwargs)
    sym_help._quantized_ops.add(output)
    return output
