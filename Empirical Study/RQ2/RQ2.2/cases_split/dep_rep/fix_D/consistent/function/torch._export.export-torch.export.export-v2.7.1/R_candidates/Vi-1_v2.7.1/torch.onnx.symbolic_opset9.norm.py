@_onnx_symbolic("aten::norm")
@symbolic_helper.parse_args("v", "t", "is", "i", "v")
def norm(g: jit_utils.GraphContext, self, p, dim, keepdim, dtype=None):
    if p == 1:
        f = symbolic_helper._reduce_op_symbolic_helper("ReduceL1")
    elif p == 2:
        f = symbolic_helper._reduce_op_symbolic_helper("ReduceL2")
    else:
        raise errors.SymbolicValueError(
            "ONNX export only p-norms with p of 1 or 2", self
        )
    result = f(g, self, dim=dim, keepdim=keepdim)
    if dtype is not None:
        dtype = symbolic_helper._get_const(dtype, "i", "dtype")
        result = g.op("Cast", result, to_i=_type_utils.JitScalarType(dtype).onnx_type())
    return result
