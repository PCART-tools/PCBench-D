@_onnx_symbolic("aten::contiguous")
@symbolic_helper.parse_args("v", "i")
def contiguous(g: jit_utils.GraphContext, input, memory_format):
    if memory_format > 2:  # allower values are any, preserve and contiguous_format
        raise errors.SymbolicValueError(
            "onnx memory_format support is not implemented", input
        )
    return input
