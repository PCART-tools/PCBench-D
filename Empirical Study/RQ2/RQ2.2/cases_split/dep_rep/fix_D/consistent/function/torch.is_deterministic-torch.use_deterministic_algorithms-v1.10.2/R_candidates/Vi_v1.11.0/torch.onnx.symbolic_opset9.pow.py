def pow(g, self, exponent):
    f_dtype = self_dtype = self.type().scalarType()
    if not sym_help._is_fp(self):
        f_dtype = "Float"
        self = g.op("Cast", self, to_i=sym_help.cast_pytorch_to_onnx[f_dtype])
    if not sym_help._is_fp(exponent):
        exponent = g.op("Cast", exponent, to_i=sym_help.cast_pytorch_to_onnx[f_dtype])
    pow = g.op("Pow", self, exponent)
    return pow
