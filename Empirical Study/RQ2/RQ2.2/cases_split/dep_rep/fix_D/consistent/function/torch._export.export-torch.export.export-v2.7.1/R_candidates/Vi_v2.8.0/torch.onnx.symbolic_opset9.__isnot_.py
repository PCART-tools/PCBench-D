@_onnx_symbolic("aten::__isnot_")
@wrap_logical_op_with_negation
def __isnot_(g: jit_utils.GraphContext, self, other):
    return __is_(g, self, other)
