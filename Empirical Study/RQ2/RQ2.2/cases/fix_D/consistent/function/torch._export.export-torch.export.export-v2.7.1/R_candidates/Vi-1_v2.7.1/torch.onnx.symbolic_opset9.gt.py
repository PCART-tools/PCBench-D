@_onnx_symbolic("aten::gt")
@symbolic_helper.quantized_args(True, True)
def gt(g: jit_utils.GraphContext, input, other):
    return _gt_impl(g, input, other)
