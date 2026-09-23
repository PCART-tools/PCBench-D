@symbolic_helper.parse_args("v", "f", "i", "t")
def quantize_per_tensor(g: jit_utils.GraphContext, input, scale, zero_point, dtype):
    kwargs = {
        "Y_scale_f": scale,
        "Y_zero_point_i": zero_point,
    }
    output = g.op("_caffe2::Int8Quantize", input, **kwargs)
    symbolic_helper._quantized_ops.add(output)
    return output
