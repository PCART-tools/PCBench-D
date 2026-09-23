@_onnx_symbolic("aten::replication_pad1d")
@_onnx_symbolic("aten::replication_pad2d")
@_onnx_symbolic("aten::replication_pad3d")
def replication_pad(g: jit_utils.GraphContext, input, padding):
    mode = "edge"
    paddings = _prepare_onnx_paddings(g, input, padding)
    return g.op("Pad", input, paddings, mode_s=mode)
