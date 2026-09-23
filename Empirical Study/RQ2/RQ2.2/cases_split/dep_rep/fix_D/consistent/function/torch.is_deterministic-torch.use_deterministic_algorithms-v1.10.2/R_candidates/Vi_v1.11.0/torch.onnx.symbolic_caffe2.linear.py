@parse_args("v", "v", "v", "f", "i")
def linear(g, input, weight, bias, scale, zero_point):
    kwargs = {
        "Y_scale_f": scale,
        "Y_zero_point_i": zero_point,
    }
    output = g.op("_caffe2::Int8FC", input, weight, bias, **kwargs)
    sym_help._quantized_ops.add(output)
    return output
