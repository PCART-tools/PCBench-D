def masked_scatter(g, self, mask, source):
    from torch.onnx.symbolic_opset9 import nonzero, expand_as, size
    index = nonzero(g, expand_as(g, mask, self))
    # NOTE: source can have more elements than needed.
    # It could also have arbitrary shape.
    # This is not supported by ONNX::ScatterND, so we need to flatten and slice source tensor.
    source = sym_help._reshape_helper(g, source, torch.LongTensor([-1]))
    source = sym_help._slice_helper(g, source,
                                    axes=torch.LongTensor([0]),
                                    starts=torch.LongTensor([0]),
                                    ends=size(g, index, torch.LongTensor([0])),
                                    dynamic_slice=True)
    return g.op("ScatterND", self, index, source)
