@_onnx_symbolic("aten::var")
def var(g: jit_utils.GraphContext, input, *args):
    var, _ = var_mean(g, input, *args)
    return var
