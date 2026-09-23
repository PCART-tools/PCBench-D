@_onnx_symbolic("aten::triu")
def triu(g: jit_utils.GraphContext, self, diagonal, out=None):
    return g.op("Trilu", self, diagonal, upper_i=1)
