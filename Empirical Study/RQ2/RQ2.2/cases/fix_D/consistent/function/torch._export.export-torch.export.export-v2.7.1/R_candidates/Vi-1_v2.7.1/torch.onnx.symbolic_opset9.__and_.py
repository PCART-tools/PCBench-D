@_onnx_symbolic("aten::__and_")
def __and_(g: jit_utils.GraphContext, input, other):
    if not symbolic_helper._is_bool(input):
        raise errors.SymbolicValueError(
            "ONNX export does NOT support exporting bitwise AND "
            "for non-boolean input values",
            input,
        )
    if not symbolic_helper._is_bool(other):
        raise errors.SymbolicValueError(
            "ONNX export does NOT support exporting bitwise AND "
            "for non-boolean input values",
            other,
        )
    return g.op("And", input, other)
