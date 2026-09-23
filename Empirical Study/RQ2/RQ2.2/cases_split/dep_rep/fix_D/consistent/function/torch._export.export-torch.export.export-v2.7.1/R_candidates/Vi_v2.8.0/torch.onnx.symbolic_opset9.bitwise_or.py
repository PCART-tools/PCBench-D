@_onnx_symbolic("aten::bitwise_or")
def bitwise_or(g, self, other):
    if not symbolic_helper._is_bool(self):
        raise errors.SymbolicValueError(
            "ONNX export does NOT support exporting bitwise OR "
            "for non-boolean input values. self: ",
            self,
        )
    if not symbolic_helper._is_bool(other):
        raise errors.SymbolicValueError(
            "ONNX export does NOT support exporting bitwise OR "
            "for non-boolean input values. other: ",
            other,
        )
    return g.op("Or", self, other)
