@_onnx_symbolic("aten::masked_fill_")
def masked_fill_(g: jit_utils.GraphContext, self, mask, value):
    return masked_fill(g, self, mask, value)
