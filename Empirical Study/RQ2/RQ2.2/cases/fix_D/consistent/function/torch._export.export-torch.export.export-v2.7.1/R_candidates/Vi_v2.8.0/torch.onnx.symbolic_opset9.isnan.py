@_onnx_symbolic("aten::isnan")
@symbolic_helper.parse_args("v")
def isnan(g: jit_utils.GraphContext, input):
    output = g.op("IsNaN", input)
    return output
