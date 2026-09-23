@_onnx_symbolic("aten::amin")
@symbolic_helper.quantized_args(True)
@symbolic_helper.parse_args("v", "is", "i")
def amin(g: jit_utils.GraphContext, self, dim, keepdim):
    return g.op("ReduceMin", self, axes_i=dim, keepdims_i=keepdim)
