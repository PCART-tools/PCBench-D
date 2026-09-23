@_onnx_symbolic("aten::hardswish")
@symbolic_helper.quantized_args(True)
@symbolic_helper.parse_args("v")
def hardswish(g: jit_utils.GraphContext, self):
    hs = hardsigmoid(g, self)
    return g.op("Mul", self, hs)
