@_onnx_symbolic("aten::take")
def take(g: jit_utils.GraphContext, self, index):
    self_flattened = symbolic_helper._reshape_helper(
        g, self, g.op("Constant", value_t=torch.tensor([-1], dtype=torch.int64))
    )
    out = index_select(g, self_flattened, 0, index)
    out = reshape_as(g, out, index)
    return out
