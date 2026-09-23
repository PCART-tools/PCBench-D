@_onnx_symbolic("aten::reshape")
@symbolic_helper.quantized_args(True)
@symbolic_helper.parse_args("v", "v")
def reshape(g: jit_utils.GraphContext, self, shape):
    # NOTE: Due to bug in ORT https://github.com/microsoft/onnxruntime/issues/10664
    #       Reshape export cannot utilize the new allowzero attribute introduced in opset 14.
    return symbolic_helper._reshape_helper(g, self, shape, allowzero=0)
