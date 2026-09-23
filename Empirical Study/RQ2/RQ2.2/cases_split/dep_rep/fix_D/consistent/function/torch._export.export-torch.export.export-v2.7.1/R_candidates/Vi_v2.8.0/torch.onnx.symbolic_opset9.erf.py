@_onnx_symbolic("aten::erf")
@symbolic_helper.parse_args("v")
def erf(g: jit_utils.GraphContext, input):
    return g.op("Erf", input)
