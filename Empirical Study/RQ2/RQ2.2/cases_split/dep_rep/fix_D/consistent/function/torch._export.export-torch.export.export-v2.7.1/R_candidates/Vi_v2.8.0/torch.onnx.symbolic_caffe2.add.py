@symbolic_helper.parse_args("v", "v", "f", "i")
def add(g: jit_utils.GraphContext, input_a, input_b, scale, zero_point):
    kwargs = {
        "Y_scale_f": scale,
        "Y_zero_point_i": zero_point,
    }
    output = g.op("_caffe2::Int8Add", input_a, input_b, **kwargs)
    symbolic_helper._quantized_ops.add(output)
    return output
