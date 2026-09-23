@_onnx_symbolic("aten::logsumexp")
@symbolic_helper.parse_args("v", "is", "i")
def logsumexp(g: jit_utils.GraphContext, input, dim, keepdim):
    return g.op("ReduceLogSumExp", input, axes_i=dim, keepdims_i=keepdim)
