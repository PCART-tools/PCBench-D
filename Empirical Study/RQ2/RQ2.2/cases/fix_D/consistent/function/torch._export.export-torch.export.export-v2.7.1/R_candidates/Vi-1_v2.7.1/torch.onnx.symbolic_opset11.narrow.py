@_onnx_symbolic("aten::narrow")
def narrow(g: jit_utils.GraphContext, input, dim, start, length):
    end = g.op("Add", start, length)
    return symbolic_helper._slice_helper(g, input, axes=dim, starts=start, ends=end)
