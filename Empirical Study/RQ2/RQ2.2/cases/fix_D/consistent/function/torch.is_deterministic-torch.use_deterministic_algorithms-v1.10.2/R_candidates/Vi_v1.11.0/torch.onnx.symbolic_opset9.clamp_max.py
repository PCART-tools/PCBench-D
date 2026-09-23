@parse_args("v", "v")
def clamp_max(g, self, max):
    if sym_help._is_constant(max):
        return g.op("Clip", self, max_f=_parse_arg(max, "f"))
    else:
        dtype = self.type().scalarType()
        max = g.op("Cast", max, to_i=sym_help.cast_pytorch_to_onnx[dtype])
        return g.op("Min", self, max)
