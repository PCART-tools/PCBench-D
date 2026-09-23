@_onnx_symbolic("aten::mm")
def mm(g: jit_utils.GraphContext, self, other):
    return g.op("Gemm", self, other, beta_f=0.0, alpha_f=1.0)
