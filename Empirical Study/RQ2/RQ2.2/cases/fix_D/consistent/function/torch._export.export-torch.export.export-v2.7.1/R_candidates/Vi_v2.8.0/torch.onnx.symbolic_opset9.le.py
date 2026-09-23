@_onnx_symbolic("aten::le")
@symbolic_helper.quantized_args(True, True)
@wrap_logical_op_with_negation
def le(g: jit_utils.GraphContext, input, other):
    return _gt_impl(g, input, other)
