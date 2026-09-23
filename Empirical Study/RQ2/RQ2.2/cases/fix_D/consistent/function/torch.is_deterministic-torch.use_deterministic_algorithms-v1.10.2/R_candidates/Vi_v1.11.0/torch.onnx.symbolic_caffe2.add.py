@parse_args("v", "v", "f", "i")
def add(g, input_a, input_b, scale, zero_point):
    kwargs = {
        "Y_scale_f": scale,
        "Y_zero_point_i": zero_point,
    }
    output = g.op("_caffe2::Int8Add", input_a, input_b, **kwargs)
    sym_help._quantized_ops.add(output)
    return output
