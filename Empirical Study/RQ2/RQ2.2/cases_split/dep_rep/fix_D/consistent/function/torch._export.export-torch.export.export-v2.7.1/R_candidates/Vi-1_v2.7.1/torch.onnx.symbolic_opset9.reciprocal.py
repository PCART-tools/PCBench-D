@_onnx_symbolic("aten::reciprocal")
def reciprocal(g: jit_utils.GraphContext, self):
    # torch.reciprocal implicitly casts to float, so we do the same.
    if not symbolic_helper._is_fp(self):
        self = g.op("Cast", self, to_i=_C_onnx.TensorProtoDataType.FLOAT)
    return g.op("Reciprocal", self)
