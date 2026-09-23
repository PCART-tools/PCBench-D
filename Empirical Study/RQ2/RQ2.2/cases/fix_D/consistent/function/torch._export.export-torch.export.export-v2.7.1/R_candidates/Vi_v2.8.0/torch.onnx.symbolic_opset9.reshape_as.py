@_onnx_symbolic("aten::reshape_as")
@symbolic_helper.quantized_args(True)
def reshape_as(g: jit_utils.GraphContext, self, other):
    shape = g.op("Shape", other)
    return reshape(g, self, shape)
