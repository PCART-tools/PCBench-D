@_onnx_symbolic("aten::std")
def std(g: jit_utils.GraphContext, input, *args):
    var, _ = var_mean(g, input, *args)
    return g.op("Sqrt", var)
