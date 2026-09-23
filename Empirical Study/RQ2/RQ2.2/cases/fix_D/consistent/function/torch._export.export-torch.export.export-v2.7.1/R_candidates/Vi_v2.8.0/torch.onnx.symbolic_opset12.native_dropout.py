@_onnx_symbolic("aten::native_dropout")
@symbolic_helper.parse_args("v", "f", "b")
def native_dropout(g: jit_utils.GraphContext, input, p, train):
    return _dropout_returns_masked_input_and_mask(g, input, p, train)
