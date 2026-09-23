def _permute_helper(g: jit_utils.GraphContext, input, axes):
    quant_args = {
        "axes_i": axes,
        "Y_scale_f": symbolic_helper._node_get(input.node(), "Y_scale"),
        "Y_zero_point_i": symbolic_helper._node_get(input.node(), "Y_zero_point"),
    }
    output = g.op("_caffe2::Int8Transpose", input, **quant_args)
    symbolic_helper._quantized_ops.add(output)
    return output
