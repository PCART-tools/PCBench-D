@_onnx_symbolic("aten::nonzero_numpy")
# Emitted from `torch.nonzero(x, as_tuple=True)`
def nonzero_numpy(g: jit_utils.GraphContext, input, _outputs=None):
    return unbind(g, opset9.nonzero(g, input), 1, _outputs=_outputs)
