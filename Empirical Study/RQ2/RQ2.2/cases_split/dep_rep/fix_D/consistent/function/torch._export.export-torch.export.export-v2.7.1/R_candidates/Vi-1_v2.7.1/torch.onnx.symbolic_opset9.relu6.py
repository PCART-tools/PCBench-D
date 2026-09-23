@_onnx_symbolic("aten::relu6")
@symbolic_helper.quantized_args(True)
def relu6(g: jit_utils.GraphContext, input):
    return clamp(g, input, 0, 6)
