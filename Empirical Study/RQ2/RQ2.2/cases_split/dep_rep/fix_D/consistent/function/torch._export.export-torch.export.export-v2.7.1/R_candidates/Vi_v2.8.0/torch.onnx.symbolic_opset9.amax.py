@_onnx_symbolic("aten::amax")
@symbolic_helper.quantized_args(True)
@symbolic_helper.parse_args("v", "is", "i")
def amax(g: jit_utils.GraphContext, self, dim, keepdim):
    return g.op("ReduceMax", self, axes_i=dim, keepdims_i=keepdim)
