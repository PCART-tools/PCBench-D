def __rshift_(g, self, other):
    # make sure to cast other to self's type
    # (when self is long, make sure that other is not float)
    if other.type().scalarType() != self.type().scalarType():
        other = g.op("Cast", other, to_i=sym_help.cast_pytorch_to_onnx[self.type().scalarType()])

    two = g.op("Constant", value_t=torch.tensor(2, dtype=torch.float32))
    # exponent (same type as self) has to be float or double in onnx::Pow
    if not sym_help._is_fp(self):
        other = g.op("Cast", other, to_i=sym_help.cast_pytorch_to_onnx["Float"])
    two_pow = g.op("Pow", two, other)
    two_pow = g.op("Cast", two_pow, to_i=sym_help.cast_pytorch_to_onnx[self.type().scalarType()])
    rshift = g.op("Div", self, two_pow)
    return rshift
