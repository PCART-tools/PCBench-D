@_onnx_symbolic("aten::celu")
def celu(g: jit_utils.GraphContext, self, alpha):
    alpha = symbolic_helper._maybe_get_const(alpha, "f")
    # if the input is of type double cast it to float
    if (
        _type_utils.JitScalarType.from_value(self, _type_utils.JitScalarType.UNDEFINED)
        == _type_utils.JitScalarType.DOUBLE
    ):
        self = g.op("Cast", self, to_i=_C_onnx.TensorProtoDataType.FLOAT)
        out = g.op("Celu", self, alpha_f=alpha)
        return g.op("Cast", out, to_i=_C_onnx.TensorProtoDataType.DOUBLE)

    return g.op("Celu", self, alpha_f=alpha)
