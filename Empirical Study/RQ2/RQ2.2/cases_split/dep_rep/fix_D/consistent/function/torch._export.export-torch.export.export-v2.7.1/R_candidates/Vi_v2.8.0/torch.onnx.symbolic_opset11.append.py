@_onnx_symbolic("aten::append")
def append(g: jit_utils.GraphContext, self, tensor):
    return g.op("SequenceInsert", self, tensor)
