@_onnx_symbolic("aten::pow")
def pow(g: jit_utils.GraphContext, self, exponent):
    f_dtype = _type_utils.JitScalarType.from_value(self)
    if not symbolic_helper._is_fp(self):
        f_dtype = _type_utils.JitScalarType.FLOAT
        self = g.op("Cast", self, to_i=f_dtype.onnx_type())
    if not symbolic_helper._is_fp(exponent):
        exponent = g.op(
            "Cast",
            exponent,
            to_i=f_dtype.onnx_type(),
        )
    pow = g.op("Pow", self, exponent)
    return pow
