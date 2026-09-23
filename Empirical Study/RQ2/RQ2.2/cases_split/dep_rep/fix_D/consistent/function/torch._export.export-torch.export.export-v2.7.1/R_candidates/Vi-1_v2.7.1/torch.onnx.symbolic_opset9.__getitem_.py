@_onnx_symbolic("aten::__getitem_")
def __getitem_(g: jit_utils.GraphContext, self, i):
    return select(g, self, g.op("Constant", value_t=torch.tensor([0])), i)
