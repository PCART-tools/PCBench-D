@_onnx_symbolic("aten::scalar_tensor")
def scalar_tensor(g: jit_utils.GraphContext, scalar, dtype, *options):
    dtype = symbolic_helper._get_const(dtype, "i", "dtype")
    if dtype is None:
        dtype = _type_utils.JitScalarType.FLOAT
    scalar = g.op("Cast", scalar, to_i=_type_utils.JitScalarType(dtype).onnx_type())
    return scalar
