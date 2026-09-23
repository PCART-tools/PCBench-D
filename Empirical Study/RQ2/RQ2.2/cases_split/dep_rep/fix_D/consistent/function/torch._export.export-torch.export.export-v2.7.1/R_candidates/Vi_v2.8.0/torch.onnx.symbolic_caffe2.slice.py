@symbolic_helper.parse_args("v", "v", "v", "v", "i")
def slice(g: jit_utils.GraphContext, input, dim, start, end, step):
    if input not in symbolic_helper._quantized_ops:
        return opset9.slice(g, input, dim, start, end, step)

    if step != 1:
        raise RuntimeError("ONNX quantized slice export only works for step 1.")
    start = symbolic_helper._parse_arg(start, "i")
    end = symbolic_helper._parse_arg(end, "i")
    dim = symbolic_helper._parse_arg(dim, "i")

    kwargs = {
        "start_idx_i": start,
        "end_idx_i": end,
        "dim_i": dim,
        "Y_scale_f": symbolic_helper._node_get(input.node(), "Y_scale"),
        "Y_zero_point_i": symbolic_helper._node_get(input.node(), "Y_zero_point"),
    }
    output = g.op("_caffe2::Int8Slice", input, **kwargs)
    symbolic_helper._quantized_ops.add(output)
    return output
