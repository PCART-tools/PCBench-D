@_onnx_symbolic("aten::gelu")
@symbolic_helper.parse_args("v", "s")
def gelu(g: jit_utils.GraphContext, self: _C.Value, approximate: str = "none"):
    return g.op("Gelu", self, approximate_s=approximate)
