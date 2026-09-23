@_onnx_symbolic("aten::dropout")
@symbolic_helper.parse_args("v", "f", "b")
def dropout(g: jit_utils.GraphContext, input, p, train):
    masked, _ = _dropout_returns_masked_input_and_mask(g, input, p, train)
    return masked
