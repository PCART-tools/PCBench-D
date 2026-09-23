@_onnx_symbolic("aten::_shape_as_tensor")
def _shape_as_tensor(g: jit_utils.GraphContext, input):
    return g.op("Shape", input)
