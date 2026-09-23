@_onnx_symbolic("aten::is_pinned")
def is_pinned(g: jit_utils.GraphContext, self, device=None):
    # Unused by ONNX.
    return None
