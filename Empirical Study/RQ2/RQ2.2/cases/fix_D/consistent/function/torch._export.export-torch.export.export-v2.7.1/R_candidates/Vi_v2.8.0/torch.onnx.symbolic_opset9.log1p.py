@_onnx_symbolic("aten::log1p")
def log1p(g: jit_utils.GraphContext, self):
    return log(g, add(g, symbolic_helper._if_scalar_type_as(torch.ones(1), self), self))
