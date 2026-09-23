@_onnx_symbolic("aten::repeat")
def repeat(g: jit_utils.GraphContext, self, repeats):
    dtype = _type_utils.JitScalarType.INT64
    shape_ = ones_like(g, repeats, dtype)
    self = g.op("Expand", self, shape_)
    return g.op("Tile", self, repeats)
