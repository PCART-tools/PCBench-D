@_onnx_symbolic("aten::cumsum")
@symbolic_helper.parse_args("v", "i", "none")
def cumsum(g: jit_utils.GraphContext, input, dim, dtype):
    symbolic_helper._onnx_opset_unsupported("cumsum", 9, 11, input)
