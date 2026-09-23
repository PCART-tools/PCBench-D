@_onnx_symbolic("aten::__isnot_")
@opset9.wrap_logical_op_with_negation  # type: ignore[has-type]
def aten__isnot_(g: jit_utils.GraphContext, self, other):
    return aten__is_(g, self, other)
