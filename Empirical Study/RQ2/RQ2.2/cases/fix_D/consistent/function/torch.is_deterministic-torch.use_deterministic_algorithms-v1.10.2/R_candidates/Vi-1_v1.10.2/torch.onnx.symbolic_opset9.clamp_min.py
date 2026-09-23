@parse_args('v', 'v')
def clamp_min(g, self, min):
    if sym_help._is_constant(min):
        return g.op("Clip", self, min_f=_parse_arg(min, 'f'))
    else:
        dtype = self.type().scalarType()
        min = g.op("Cast", min, to_i=sym_help.cast_pytorch_to_onnx[dtype])
        return g.op("Max", self, min)
