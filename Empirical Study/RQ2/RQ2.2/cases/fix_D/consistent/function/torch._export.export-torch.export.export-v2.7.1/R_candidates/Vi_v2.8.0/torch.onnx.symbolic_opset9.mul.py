@_onnx_symbolic("aten::mul")
def mul(g: jit_utils.GraphContext, self, other):
    if symbolic_helper._is_bool(self) and symbolic_helper._is_bool(other):
        # ONNX Mul doesn't support Boolean, so use And as an equivalent operator.
        return g.op("And", self, other)
    else:
        return g.op("Mul", self, other)
