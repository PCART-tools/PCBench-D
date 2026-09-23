def tensor(g, data, dtype=None, device=None, requires_grad=False):
    dtype = sym_help._get_const(dtype, "i", "dtype")
    if sym_help._is_packed_list(data):
        if dtype is None:
            dtype = sym_help._unpack_list(data)[0].type().scalarType()
            dtype = sym_help.scalar_type_to_onnx.index(sym_help.cast_pytorch_to_onnx[dtype])
        input_list = list()
        for t in sym_help._unpack_list(data):
            shape_reference = g.op("Constant", value_t=torch.LongTensor([1]))
            t = sym_help._reshape_helper(g, t, shape_reference)
            t = g.op("Cast", t, to_i=sym_help.scalar_type_to_onnx[dtype])
            input_list.append(t)
        return g.op("Concat", *input_list, axis_i=0)
    else:
        if dtype is None:
            dtype = data.type().scalarType()
            dtype = sym_help.scalar_type_to_onnx.index(sym_help.cast_pytorch_to_onnx[dtype])
        if sym_help._is_list(data) and (sym_help._is_tensor_list(data) or sym_help._is_scalar_list(data)):
            data = g.op("ConcatFromSequence", data, axis_i=0, new_axis_i=1)
    return g.op("Cast", data, to_i=sym_help.scalar_type_to_onnx[dtype])
