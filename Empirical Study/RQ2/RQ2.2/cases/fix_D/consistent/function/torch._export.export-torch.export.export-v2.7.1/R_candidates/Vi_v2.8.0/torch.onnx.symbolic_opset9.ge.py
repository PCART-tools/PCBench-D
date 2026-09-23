@_onnx_symbolic("aten::ge")
@symbolic_helper.quantized_args(True, True)
@wrap_logical_op_with_negation
def ge(g: jit_utils.GraphContext, input, other):
    return _lt_impl(g, input, other)
