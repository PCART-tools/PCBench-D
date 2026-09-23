@_onnx_symbolic("aten::full")
def full(
    g: jit_utils.GraphContext, sizes, value, dtype, layout, device, pin_memory=False
):
    const_value = symbolic_helper._maybe_get_const(value, "t")
    if symbolic_helper._is_value(const_value):
        dtype = _type_utils.JitScalarType.FLOAT if dtype is None else dtype
        tmp = zeros(g, sizes, dtype, layout, device)
        return add(g, tmp, value, g.op("Constant", value_t=torch.tensor(1)))
    else:
        dtype = symbolic_helper._get_const(dtype, "i", "dtype")
        if dtype is None:
            scalar_type = _type_utils.JitScalarType.FLOAT
        else:
            scalar_type = _type_utils.JitScalarType(dtype)
        sizes_ = symbolic_helper._maybe_get_const(sizes, "is")
        if isinstance(sizes_, list) and len(sizes_) == 0:
            sizes = g.op("Constant", value_t=torch.tensor([]).to(torch.int64))
        return g.op(
            "ConstantOfShape",
            sizes,
            value_t=const_value.view(1).to(scalar_type.dtype()),
        )
