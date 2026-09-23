def full_like(g, input, fill_value, dtype=None, layout=None, device=None, pin_memory=False, memory_format=None):
    fill_value = sym_help._maybe_get_const(fill_value, "f")
    dtype = sym_help._get_const(dtype, "i", "dtype")
    dtype = ScalarType.FLOAT if dtype is None else dtype
    if sym_help._is_value(fill_value):
        tmp = zeros_like(g, input, dtype, layout, device)
        fill_value = g.op("Cast", fill_value, to_i=sym_help.scalar_type_to_onnx[dtype])
        return add(g, tmp, fill_value, g.op("Constant", value_t=torch.tensor(1)))
    else:
        shape = g.op("Shape", input)
        return g.op("ConstantOfShape", shape,
                    value_t=torch.tensor([fill_value]).to(sym_help.scalar_type_to_pytorch_type[dtype]))
