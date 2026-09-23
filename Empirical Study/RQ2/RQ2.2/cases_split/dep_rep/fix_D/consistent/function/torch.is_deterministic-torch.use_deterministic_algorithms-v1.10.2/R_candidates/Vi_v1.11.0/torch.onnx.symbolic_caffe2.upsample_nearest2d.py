def upsample_nearest2d(g, input, output_size, align_corners=None, scales_h=None, scales_w=None):
    if input not in sym_help._quantized_ops:
        from torch.onnx.symbolic_opset9 import upsample_nearest2d as upsample_nearest2d_impl
        return upsample_nearest2d_impl(g, input, output_size, align_corners)

    output_size = sym_help._parse_arg(output_size, "is")
    kwargs = {
        "output_size_i": output_size,
        "Y_scale_f": input.node()["Y_scale"],
        "Y_zero_point_i": input.node()["Y_zero_point"],
    }
    input = nchw2nhwc(g, input)
    output = g.op("_caffe2::Int8ResizeNearest", input, **kwargs)
    output = nhwc2nchw(g, output)
    sym_help._quantized_ops.add(output)
    return output
