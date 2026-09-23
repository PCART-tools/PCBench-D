@_onnx_symbolic("aten::as_tensor")
def as_tensor(g: jit_utils.GraphContext, data, dtype=None, device=None):
    return tensor(g, data, dtype, device)
