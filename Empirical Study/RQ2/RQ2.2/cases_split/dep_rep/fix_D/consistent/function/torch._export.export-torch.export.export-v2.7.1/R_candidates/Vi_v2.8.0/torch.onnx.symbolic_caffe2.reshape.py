def reshape(g: jit_utils.GraphContext, input, shape):
    if input not in symbolic_helper._quantized_ops:
        return opset9.reshape(g, input, shape)

    kwargs = {
        "Y_scale_f": symbolic_helper._node_get(input.node(), "Y_scale"),
        "Y_zero_point_i": symbolic_helper._node_get(input.node(), "Y_zero_point"),
    }
    output = g.op("_caffe2::Int8Reshape", input, shape, **kwargs)
    symbolic_helper._quantized_ops.add(output)
    return output
