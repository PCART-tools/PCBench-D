@_onnx_symbolic("aten::nonzero")
@symbolic_helper.parse_args("v")
def nonzero(g: jit_utils.GraphContext, input):
    """Emitted from `torch.nonzero(x, as_tuple=False)`"""
    return t(g, g.op("NonZero", input))
