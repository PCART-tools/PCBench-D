@_onnx_symbolic("aten::_unique2")
@symbolic_helper.parse_args("v", "i", "i", "i")
def _unique2(g: jit_utils.GraphContext, input, sorted, return_inverse, return_counts):
    symbolic_helper._onnx_opset_unsupported("_unique2", 9, 11, input)
