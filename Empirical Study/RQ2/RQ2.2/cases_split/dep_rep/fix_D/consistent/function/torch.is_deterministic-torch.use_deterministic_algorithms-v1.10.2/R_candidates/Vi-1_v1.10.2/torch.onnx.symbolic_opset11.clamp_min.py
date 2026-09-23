@parse_args('v', 'v')
def clamp_min(g, self, min):
    dtype = self.type().scalarType()
    min = g.op("Cast", min, to_i=sym_help.cast_pytorch_to_onnx[dtype])
    if sym_help._get_tensor_rank(min) == 0:
        max = unused(g)
        return g.op("Clip", self, min, max)
    else:
        return g.op("Max", self, min)
