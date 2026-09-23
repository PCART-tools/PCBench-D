@_onnx_symbolic("aten::all")
def _all(g: jit_utils.GraphContext, *args):
    input = g.op("Not", args[0])
    # aten::all(Tensor self)
    if len(args) == 1:
        return g.op("Not", _any(g, input))
    # aten::all(Tensor self, int[]? dim, bool keepdim)
    else:
        return g.op("Not", _any(g, input, args[1], args[2]))
