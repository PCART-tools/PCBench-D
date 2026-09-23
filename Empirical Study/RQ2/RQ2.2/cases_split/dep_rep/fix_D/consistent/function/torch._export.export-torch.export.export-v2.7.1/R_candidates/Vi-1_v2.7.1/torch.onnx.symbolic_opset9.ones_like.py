@_onnx_symbolic("aten::ones_like")
@symbolic_helper.parse_args("v", "i", "v", "v", "v", "v")
def ones_like(
    g: jit_utils.GraphContext,
    input,
    dtype=None,
    layout=None,
    device=None,
    pin_memory=False,
    memory_format=None,
):
    shape = g.op("Shape", input)
    if symbolic_helper._is_none(dtype):
        scalar_type = _type_utils.JitScalarType.from_value(
            input, _type_utils.JitScalarType.FLOAT
        )
    else:
        scalar_type = _type_utils.JitScalarType(dtype)
    return g.op(
        "ConstantOfShape",
        shape,
        value_t=torch.tensor([1], dtype=scalar_type.dtype()),
    )
