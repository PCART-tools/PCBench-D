def _permute_helper(g, input, axes):
    quant_args = {
        "axes_i": axes,
        "Y_scale_f": input.node()["Y_scale"],
        "Y_zero_point_i": input.node()["Y_zero_point"],
    }
    output = g.op("_caffe2::Int8Transpose", input, **quant_args)
    sym_help._quantized_ops.add(output)
    return output
