@_onnx_symbolic("aten::dequantize")
def dequantize(g: jit_utils.GraphContext, input):
    return symbolic_helper.dequantize_helper(g, input)[0]
