@_onnx_symbolic("aten::tril")
def tril(g: jit_utils.GraphContext, self, diagonal, out=None):
    return g.op("Trilu", self, diagonal, upper_i=0)
