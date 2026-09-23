def cat(g: jit_utils.GraphContext, tensor_list, dim, scale=None, zero_point=None):
    tensors = symbolic_helper._unpack_list(tensor_list)
    input = tensors[0]
    if input not in symbolic_helper._quantized_ops:
        return opset9.cat(g, tensor_list, dim)

    dim = symbolic_helper._parse_arg(dim, "i")
    kwargs = {
        "Y_scale_f": tensors[0].node()["Y_scale"],
        "Y_zero_point_i": tensors[0].node()["Y_zero_point"],
    }
    output = g.op("_caffe2::Int8Concat", *tensors, axis_i=dim, **kwargs)
    symbolic_helper._quantized_ops.add(output)
    return output
