@_onnx_symbolic("aten::full_like")
def full_like(
    g: jit_utils.GraphContext,
    input,
    fill_value,
    dtype=None,
    layout=None,
    device=None,
    pin_memory=False,
    memory_format=None,
):
    fill_value = symbolic_helper._maybe_get_const(fill_value, "f")
    dtype = symbolic_helper._get_const(dtype, "i", "dtype")
    if dtype is None:
        scalar_type = _type_utils.JitScalarType.from_value(
            input, _type_utils.JitScalarType.FLOAT
        )
    else:
        scalar_type = _type_utils.JitScalarType(dtype)
    if symbolic_helper._is_value(fill_value):
        tmp = zeros_like(g, input, dtype, layout, device)
        fill_value = g.op("Cast", fill_value, to_i=scalar_type.onnx_type())
        return add(g, tmp, fill_value, g.op("Constant", value_t=torch.tensor(1)))
    else:
        shape = g.op("Shape", input)
        return g.op(
            "ConstantOfShape",
            shape,
            value_t=torch.tensor([fill_value], dtype=scalar_type.dtype()),
        )
