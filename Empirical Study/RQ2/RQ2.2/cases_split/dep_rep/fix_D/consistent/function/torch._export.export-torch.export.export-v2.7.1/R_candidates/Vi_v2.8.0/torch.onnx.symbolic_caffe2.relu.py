@symbolic_helper.parse_args("v")
def relu(g: jit_utils.GraphContext, input):
    if input not in symbolic_helper._quantized_ops:
        return opset9.relu(g, input)
    kwargs = {
        "Y_scale_f": symbolic_helper._node_get(input.node(), "Y_scale"),
        "Y_zero_point_i": symbolic_helper._node_get(input.node(), "Y_zero_point"),
    }
    output = g.op("_caffe2::Int8Relu", input, **kwargs)
    symbolic_helper._quantized_ops.add(output)
    return output
