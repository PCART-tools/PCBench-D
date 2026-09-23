@_onnx_symbolic("aten::zeros")
@symbolic_helper.parse_args("v", "i", "v", "v", "v")
def zeros(g: jit_utils.GraphContext, sizes, dtype, layout, device, pin_memory=False):
    # NOTE: no way to set device, layout and pin_memory in ONNX, so we ignore it
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
        value_t=torch.tensor([0], dtype=scalar_type.dtype()),
    )
