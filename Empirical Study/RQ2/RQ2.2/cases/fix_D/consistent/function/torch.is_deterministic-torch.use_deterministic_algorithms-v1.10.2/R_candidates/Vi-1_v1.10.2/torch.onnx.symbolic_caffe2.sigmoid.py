@parse_args("v")
def sigmoid(g, input):
    if input not in sym_help._quantized_ops:
        from torch.onnx.symbolic_opset9 import sigmoid
        return sigmoid(g, input)
    # Caffe2 expects the output scale to be 1/2^8
    # and output zero_point to be 0 (quint8 type)
    out_scale = 1.0 / 256
    zero_point = 0
    kwargs = {
        "Y_scale_f": out_scale,
        "Y_zero_point_i": zero_point,
    }
    output = g.op("_caffe2::Int8Sigmoid", input, **kwargs)
    sym_help._quantized_ops.add(output)
    return output
