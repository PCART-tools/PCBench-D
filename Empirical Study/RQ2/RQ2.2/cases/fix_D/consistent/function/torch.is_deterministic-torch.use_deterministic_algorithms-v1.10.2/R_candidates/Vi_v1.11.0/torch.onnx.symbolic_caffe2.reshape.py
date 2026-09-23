def reshape(g, input, shape):
    if input not in sym_help._quantized_ops:
        from torch.onnx.symbolic_opset9 import reshape
        return reshape(g, input, shape)

    kwargs = {
        "Y_scale_f": input.node()["Y_scale"],
        "Y_zero_point_i": input.node()["Y_zero_point"],
    }
    output = g.op("_caffe2::Int8Reshape", input, shape, **kwargs)
    sym_help._quantized_ops.add(output)
    return output
