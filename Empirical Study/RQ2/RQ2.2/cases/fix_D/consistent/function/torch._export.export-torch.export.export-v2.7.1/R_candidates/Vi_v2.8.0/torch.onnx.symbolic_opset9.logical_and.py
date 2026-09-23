@_onnx_symbolic("aten::logical_and")
@wrap_logical_op_with_cast_to("Bool")
def logical_and(g: jit_utils.GraphContext, input, other):
    return g.op("And", input, other)
