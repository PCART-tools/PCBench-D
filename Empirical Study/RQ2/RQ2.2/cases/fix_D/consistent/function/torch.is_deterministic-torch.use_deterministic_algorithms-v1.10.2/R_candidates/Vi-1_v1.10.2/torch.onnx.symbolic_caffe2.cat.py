def cat(g, tensor_list, dim, scale=None, zero_point=None):
    tensors = sym_help._unpack_list(tensor_list)
    input = tensors[0]
    if input not in sym_help._quantized_ops:
        from torch.onnx.symbolic_opset9 import cat
        return cat(g, tensor_list, dim)

    dim = sym_help._parse_arg(dim, "i")
    kwargs = {
        "Y_scale_f": tensors[0].node()["Y_scale"],
        "Y_zero_point_i": tensors[0].node()["Y_zero_point"],
    }
    output = g.op("_caffe2::Int8Concat", *tensors, axis_i=dim, **kwargs)
    sym_help._quantized_ops.add(output)
    return output
