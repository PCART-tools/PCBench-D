@symbolic_helper.parse_args("v")
def sigmoid(g: jit_utils.GraphContext, input):
    if input not in symbolic_helper._quantized_ops:
        return opset9.sigmoid(g, input)
    # Caffe2 expects the output scale to be 1/2^8
    # and output zero_point to be 0 (quint8 type)
    out_scale = 1.0 / 256
    zero_point = 0
    kwargs = {
        "Y_scale_f": out_scale,
        "Y_zero_point_i": zero_point,
    }
    output = g.op("_caffe2::Int8Sigmoid", input, **kwargs)
    symbolic_helper._quantized_ops.add(output)
    return output
