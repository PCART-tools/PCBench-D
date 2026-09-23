@_onnx_symbolic("aten::masked_select")
def masked_select(g: jit_utils.GraphContext, self, mask):
    index = opset9.nonzero(g, opset9.expand_as(g, mask, self))
    return g.op("GatherND", self, index)
