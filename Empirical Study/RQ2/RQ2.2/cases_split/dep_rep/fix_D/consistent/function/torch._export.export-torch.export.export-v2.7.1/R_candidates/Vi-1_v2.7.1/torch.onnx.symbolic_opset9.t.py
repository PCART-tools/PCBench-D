@_onnx_symbolic("aten::t")
def t(g: jit_utils.GraphContext, self):
    rank = symbolic_helper._get_tensor_rank(self)
    if rank is None or rank < 2:
        # The transpose of a 1d or 0d tensor is itself. ONNX does not define the behavior
        # clearly and onnxruntime fails on these cases. So we add an Identity node to
        # mirror the behavior of eager mode.
        return g.op("Identity", self)
    return g.op("Transpose", self, perm_i=(1, 0))
