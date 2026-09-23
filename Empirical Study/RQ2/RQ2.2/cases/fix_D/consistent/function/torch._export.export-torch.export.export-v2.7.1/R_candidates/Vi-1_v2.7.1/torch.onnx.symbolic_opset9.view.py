@_onnx_symbolic("aten::view")
@symbolic_helper.quantized_args(True)
def view(g: jit_utils.GraphContext, self, size):
    return reshape(g, self, size)
