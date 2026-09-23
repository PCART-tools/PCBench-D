@_onnx_symbolic("aten::masked_scatter")
def masked_scatter(g: jit_utils.GraphContext, self, mask, source):
    index = opset9.nonzero(g, opset9.expand_as(g, mask, self))
    # NOTE: source can have more elements than needed.
    # It could also have arbitrary shape.
    # This is not supported by ONNX::ScatterND, so we need to flatten and slice source tensor.
    source = symbolic_helper._reshape_helper(g, source, torch.LongTensor([-1]))
    source = symbolic_helper._slice_helper(
        g,
        source,
        axes=torch.LongTensor([0]),
        starts=torch.LongTensor([0]),
        ends=opset9.size(g, index, torch.LongTensor([0])),
    )
    return g.op("ScatterND", self, index, source)
