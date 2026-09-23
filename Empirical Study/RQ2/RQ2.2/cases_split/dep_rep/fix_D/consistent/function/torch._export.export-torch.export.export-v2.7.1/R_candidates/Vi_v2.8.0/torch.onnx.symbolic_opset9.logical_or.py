@_onnx_symbolic("aten::logical_or")
@wrap_logical_op_with_cast_to("Bool")
def logical_or(g: jit_utils.GraphContext, input, other):
    return g.op("Or", input, other)
