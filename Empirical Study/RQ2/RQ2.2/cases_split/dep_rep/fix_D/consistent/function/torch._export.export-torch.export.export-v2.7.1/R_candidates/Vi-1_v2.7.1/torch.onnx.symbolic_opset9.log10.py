@_onnx_symbolic("aten::log10")
def log10(g: jit_utils.GraphContext, self):
    _ln10 = 2.30258509299404568401
    return g.op("Div", log(g, self), g.op("Constant", value_t=torch.tensor([_ln10])))
