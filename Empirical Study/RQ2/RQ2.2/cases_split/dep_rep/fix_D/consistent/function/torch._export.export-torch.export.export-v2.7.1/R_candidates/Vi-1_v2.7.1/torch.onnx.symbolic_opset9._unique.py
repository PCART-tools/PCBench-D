@_onnx_symbolic("aten::_unique")
@symbolic_helper.parse_args("v", "i", "i")
def _unique(g: jit_utils.GraphContext, input, sorted, return_inverse):
    return symbolic_helper._onnx_unsupported("_unique", input)
