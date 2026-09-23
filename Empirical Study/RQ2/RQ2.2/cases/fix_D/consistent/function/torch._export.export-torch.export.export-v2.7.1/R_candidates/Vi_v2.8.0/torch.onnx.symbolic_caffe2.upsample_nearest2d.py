def upsample_nearest2d(
    g: jit_utils.GraphContext,
    input,
    output_size,
    align_corners=None,
    scales_h=None,
    scales_w=None,
):
    if input not in symbolic_helper._quantized_ops:
        return opset9.upsample_nearest2d(g, input, output_size, align_corners)  # type: ignore[attr-defined]

    output_size = symbolic_helper._parse_arg(output_size, "is")
    kwargs = {
        "output_size_i": output_size,
        "Y_scale_f": symbolic_helper._node_get(input.node(), "Y_scale"),
        "Y_zero_point_i": symbolic_helper._node_get(input.node(), "Y_zero_point"),
    }
    input = nchw2nhwc(g, input)
    output = g.op("_caffe2::Int8ResizeNearest", input, **kwargs)
    output = nhwc2nchw(g, output)
    symbolic_helper._quantized_ops.add(output)
    return output
