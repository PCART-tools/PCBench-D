@_onnx_symbolic("aten::log_sigmoid")
@symbolic_helper.parse_args("v")
def log_sigmoid(g: jit_utils.GraphContext, input):
    p = g.op("Sigmoid", input)
    return g.op("Log", p)
