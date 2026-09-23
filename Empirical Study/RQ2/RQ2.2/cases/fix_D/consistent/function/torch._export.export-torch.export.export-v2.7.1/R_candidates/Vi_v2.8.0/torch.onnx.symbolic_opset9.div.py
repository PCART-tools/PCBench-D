@_onnx_symbolic("aten::div")
def div(g: jit_utils.GraphContext, self, other, *args):
    if len(args) == 0:
        return true_divide(g, self, other)
    else:
        return _div_rounding_mode(g, self, other, *args)
