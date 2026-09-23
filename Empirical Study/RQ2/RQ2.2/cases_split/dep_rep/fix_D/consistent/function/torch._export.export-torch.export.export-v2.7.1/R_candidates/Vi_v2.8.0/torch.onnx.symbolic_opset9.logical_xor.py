@_onnx_symbolic("aten::logical_xor")
@wrap_logical_op_with_cast_to("Bool")
def logical_xor(g: jit_utils.GraphContext, input, other):
    return g.op("Xor", input, other)
