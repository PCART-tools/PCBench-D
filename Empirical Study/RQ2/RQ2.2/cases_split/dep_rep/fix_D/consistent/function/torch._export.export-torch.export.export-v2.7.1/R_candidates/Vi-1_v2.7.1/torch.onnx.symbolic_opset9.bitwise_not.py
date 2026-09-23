@_onnx_symbolic("aten::bitwise_not")
def bitwise_not(g: jit_utils.GraphContext, input):
    if not symbolic_helper._is_bool(input):
        raise errors.SymbolicValueError(
            "ONNX export does NOT support exporting bitwise Not "
            "for non-boolean input values",
            input,
        )
    return g.op("Not", input)
