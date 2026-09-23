@_onnx_symbolic("aten::rrelu")
@symbolic_helper.parse_args("v", "f", "f", "i", "none")
def rrelu(g: jit_utils.GraphContext, input, lower, upper, training, generator):
    if not training:
        slope = (upper + lower) / 2.0
        return g.op("LeakyRelu", input, alpha_f=slope)
    p = g.op("RandomUniformLike", input, high_f=upper, low_f=lower)
    return g.op("PRelu", input, p)
