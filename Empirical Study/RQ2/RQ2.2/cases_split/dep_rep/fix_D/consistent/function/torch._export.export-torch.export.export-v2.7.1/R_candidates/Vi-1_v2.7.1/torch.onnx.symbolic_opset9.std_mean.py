@_onnx_symbolic("aten::std_mean")
def std_mean(g: jit_utils.GraphContext, input, *args):
    var, mean = var_mean(g, input, *args)
    return g.op("Sqrt", var), mean
