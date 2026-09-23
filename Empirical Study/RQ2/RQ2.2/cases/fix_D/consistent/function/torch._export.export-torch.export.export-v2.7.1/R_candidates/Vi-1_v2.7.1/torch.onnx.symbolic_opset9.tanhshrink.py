@_onnx_symbolic("aten::tanhshrink")
@symbolic_helper.parse_args("v")
def tanhshrink(g: jit_utils.GraphContext, self):
    return g.op("Sub", self, tanh(g, self))
