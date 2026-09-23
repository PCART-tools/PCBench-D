@parse_args("v")
def relu(g, input):
    if input not in sym_help._quantized_ops:
        from torch.onnx.symbolic_opset9 import relu
        return relu(g, input)
    kwargs = {
        "Y_scale_f": input.node()["Y_scale"],
        "Y_zero_point_i": input.node()["Y_zero_point"],
    }
    output = g.op("_caffe2::Int8Relu", input, **kwargs)
    sym_help._quantized_ops.add(output)
    return output
