@_onnx_symbolic("aten::frobenius_norm")
@symbolic_helper.parse_args("v", "is", "b")
def frobenius_norm(g: jit_utils.GraphContext, self, dim=None, keepdim=False):
    sqr = g.op("Mul", self, self)
    sumsqr = symbolic_helper._reducesum_helper(g, sqr, axes_i=dim, keepdims_i=keepdim)
    return g.op("Sqrt", sumsqr)
