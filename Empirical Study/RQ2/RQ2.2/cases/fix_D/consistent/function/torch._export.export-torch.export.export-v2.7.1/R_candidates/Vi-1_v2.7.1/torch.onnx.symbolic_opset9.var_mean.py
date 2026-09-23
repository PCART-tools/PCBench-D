@_onnx_symbolic("aten::var_mean")
def var_mean(g: jit_utils.GraphContext, input, *args):
    if len(args) == 1:
        return _var_mean(g, input, None, args[0], None)
    else:
        return _var_mean(g, input, *args)
