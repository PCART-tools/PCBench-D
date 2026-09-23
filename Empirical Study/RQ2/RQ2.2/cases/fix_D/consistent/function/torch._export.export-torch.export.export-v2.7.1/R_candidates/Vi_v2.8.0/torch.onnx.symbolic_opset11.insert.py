@_onnx_symbolic("aten::insert")
def insert(g: jit_utils.GraphContext, self, pos, tensor):
    return g.op("SequenceInsert", self, tensor, pos)
