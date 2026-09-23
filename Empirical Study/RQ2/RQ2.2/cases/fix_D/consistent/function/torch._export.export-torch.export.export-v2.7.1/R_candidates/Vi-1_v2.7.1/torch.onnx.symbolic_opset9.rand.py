@_onnx_symbolic("aten::rand")
def rand(g: jit_utils.GraphContext, shapes, dtype, *options):
    dtype = symbolic_helper._get_const(dtype, "i", "dtype")
    if dtype is None:
        scalar_type = _type_utils.JitScalarType.FLOAT
    else:
        scalar_type = _type_utils.JitScalarType(dtype)
    shape = symbolic_helper._maybe_get_const(shapes, "is")
    if symbolic_helper._is_value(shape):
        shape_const = g.op(
            "ConstantOfShape",
            shapes,
            value_t=torch.tensor([0], dtype=torch.float),
        )
        return g.op(
            "RandomUniformLike",
            shape_const,
            dtype_i=scalar_type.onnx_type(),
        )
    return g.op(
        "RandomUniform",
        shape_i=shape,
        dtype_i=scalar_type.onnx_type(),
    )
