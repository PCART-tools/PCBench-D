@parse_args("v", "v")
def clamp_max(g, self, max):
    dtype = self.type().scalarType()
    max = g.op("Cast", max, to_i=sym_help.cast_pytorch_to_onnx[dtype])
    if sym_help._get_tensor_rank(max) == 0:
        min = unused(g)
        return g.op("Clip", self, min, max)
    else:
        return g.op("Min", self, max)
