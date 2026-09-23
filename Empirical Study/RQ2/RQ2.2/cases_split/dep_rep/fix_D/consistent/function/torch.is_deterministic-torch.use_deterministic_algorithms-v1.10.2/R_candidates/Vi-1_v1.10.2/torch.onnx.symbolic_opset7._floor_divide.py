def _floor_divide(g, self, other):
    if sym_help._is_fp(self) or sym_help._is_fp(other):
        out = sym_opset9.true_divide(g, self, other)
        return g.op("Floor", out)
    else:
        raise RuntimeError("Integer floor division requires ONNX opset 9 or greater")
