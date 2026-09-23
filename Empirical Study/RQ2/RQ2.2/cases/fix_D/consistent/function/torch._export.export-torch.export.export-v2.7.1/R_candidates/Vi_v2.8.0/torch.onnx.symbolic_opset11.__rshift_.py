@_onnx_symbolic("aten::bitwise_right_shift")
@_onnx_symbolic("aten::__rshift_")
def __rshift_(g: jit_utils.GraphContext, self, other):
    # make sure to cast other to self's type
    # (when self is long, make sure that other is not float)
    if _type_utils.JitScalarType.from_value(
        other, _type_utils.JitScalarType.UNDEFINED
    ) != _type_utils.JitScalarType.from_value(self):
        other = g.op(
            "Cast",
            other,
            to_i=_type_utils.JitScalarType.from_value(self).onnx_type(),
        )

    if (
        _type_utils.JitScalarType.from_value(self, _type_utils.JitScalarType.UNDEFINED)
        == _type_utils.JitScalarType.UINT8
    ):
        return g.op("BitShift", self, other, direction_s="RIGHT")

    two = g.op("Constant", value_t=torch.tensor(2, dtype=torch.float32))
    # exponent (same type as self) has to be float or double in onnx::Pow
    if not symbolic_helper._is_fp(self):
        other = g.op("Cast", other, to_i=_C_onnx.TensorProtoDataType.FLOAT)
    two_pow = g.op("Pow", two, other)
    two_pow = g.op(
        "Cast",
        two_pow,
        to_i=_type_utils.JitScalarType.from_value(self).onnx_type(),
    )
    rshift = g.op("Div", self, two_pow)
    return rshift
