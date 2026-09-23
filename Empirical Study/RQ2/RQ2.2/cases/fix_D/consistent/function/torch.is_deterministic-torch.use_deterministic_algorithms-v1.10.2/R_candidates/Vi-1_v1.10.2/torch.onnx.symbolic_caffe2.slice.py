@parse_args("v", "v", "v", "v", "i")
def slice(g, input, dim, start, end, step):
    if input not in sym_help._quantized_ops:
        from torch.onnx.symbolic_opset9 import slice
        return slice(g, input, dim, start, end, step)

    if step != 1:
        raise RuntimeError("ONNX quantized slice export only works for step 1.")
    start = sym_help._parse_arg(start, "i")
    end = sym_help._parse_arg(end, "i")
    dim = sym_help._parse_arg(dim, "i")

    kwargs = {
        "start_idx_i": start,
        "end_idx_i": end,
        "dim_i": dim,
        "Y_scale_f": input.node()["Y_scale"],
        "Y_zero_point_i": input.node()["Y_zero_point"],
    }
    output = g.op("_caffe2::Int8Slice", input, **kwargs)
    sym_help._quantized_ops.add(output)
    return output
