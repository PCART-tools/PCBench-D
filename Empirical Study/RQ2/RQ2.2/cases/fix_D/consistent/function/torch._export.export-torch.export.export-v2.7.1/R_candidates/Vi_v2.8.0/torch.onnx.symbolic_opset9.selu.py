@_onnx_symbolic("aten::selu")
@symbolic_helper.quantized_args(True)
def selu(g: jit_utils.GraphContext, input):
    return g.op("Selu", input)
