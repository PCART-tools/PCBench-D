@_onnx_symbolic("aten::lift")
def lift(g: jit_utils.GraphContext, self):
    # at::lift() is a no-op from the perspective of tracing for onnx
    return self
