@_onnx_symbolic("aten::ne")
@symbolic_helper.quantized_args(True, True)
@wrap_logical_op_with_negation
def ne(g: jit_utils.GraphContext, self, other):
    return eq(g, self, other)
