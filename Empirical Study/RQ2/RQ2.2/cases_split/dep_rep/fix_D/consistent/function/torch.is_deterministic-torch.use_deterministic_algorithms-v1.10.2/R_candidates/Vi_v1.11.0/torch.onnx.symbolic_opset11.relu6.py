def relu6(g, input):
    relu = g.op("Relu", input)
    dtype = input.type().scalarType()
    if dtype is None:
        dtype = ScalarType.FLOAT
    else:
        dtype = sym_help.scalar_type_to_onnx.index(sym_help.cast_pytorch_to_onnx[dtype])
    min_val = g.op("Constant", value_t=torch.tensor(0, dtype=sym_help.scalar_type_to_pytorch_type[dtype]))
    max_val = g.op("Constant", value_t=torch.tensor(6, dtype=sym_help.scalar_type_to_pytorch_type[dtype]))
    return clamp(g, relu, min_val, max_val)
