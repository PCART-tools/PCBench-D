@_onnx_symbolic("aten::hardswish")
@symbolic_helper.parse_args("v")
def hardswish(g: jit_utils.GraphContext, self):
    return g.op("HardSwish", self)
