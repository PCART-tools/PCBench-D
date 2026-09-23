@_onnx_symbolic("aten::reshape")
@symbolic_helper.quantized_args(True)
def reshape(g: jit_utils.GraphContext, self, shape):
    return symbolic_helper._reshape_helper(g, self, shape)
