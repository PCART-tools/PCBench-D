@_onnx_symbolic("aten::softplus")
def softplus(g: jit_utils.GraphContext, self, beta, threshold):
    beta_const = symbolic_helper._maybe_get_const(beta, "f")
    if beta_const != 1:
        return g.op("Div", g.op("Softplus", g.op("Mul", self, beta)), beta)
    return g.op("Softplus", self)
