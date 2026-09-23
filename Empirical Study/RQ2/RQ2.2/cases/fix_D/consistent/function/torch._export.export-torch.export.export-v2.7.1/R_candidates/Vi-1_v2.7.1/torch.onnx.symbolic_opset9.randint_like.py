@_onnx_symbolic("aten::randint_like")
def randint_like(g: jit_utils.GraphContext, self, low, high, dtype, *options):
    dtype = symbolic_helper._get_const(dtype, "i", "dtype")
    low_i = symbolic_helper._get_const(low, "i", "low")
    high_i = symbolic_helper._get_const(high, "i", "high")
    if dtype is None:
        scalar_type = _type_utils.JitScalarType.INT64
    else:
        scalar_type = _type_utils.JitScalarType(dtype)
    if low_i is None:
        raise symbolic_helper._onnx_unsupported("randint", low)
    if high_i is None:
        raise symbolic_helper._onnx_unsupported("randint", high)

    randn = g.op(
        "RandomUniformLike",
        self,
        low_f=low_i,
        high_f=high_i,
    )

    # cast to integer type
    int_dtype = _type_utils.JitScalarType.INT64
    randint = g.op("Cast", randn, to_i=int_dtype.onnx_type())
    if int_dtype != scalar_type:
        randint = g.op("Cast", randint, to_i=scalar_type.onnx_type())
    return randint
