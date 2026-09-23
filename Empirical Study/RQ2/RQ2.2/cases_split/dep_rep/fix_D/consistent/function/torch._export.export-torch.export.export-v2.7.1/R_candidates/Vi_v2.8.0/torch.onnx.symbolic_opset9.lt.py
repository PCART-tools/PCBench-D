@_onnx_symbolic("aten::lt")
@symbolic_helper.quantized_args(True, True)
def lt(g: jit_utils.GraphContext, input, other):
    return _lt_impl(g, input, other)
