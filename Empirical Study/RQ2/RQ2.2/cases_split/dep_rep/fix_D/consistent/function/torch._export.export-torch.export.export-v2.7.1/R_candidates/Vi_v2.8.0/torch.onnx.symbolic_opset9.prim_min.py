@_onnx_symbolic("prim::min")
def prim_min(g: jit_utils.GraphContext, self, other=None):
    if not other:
        if symbolic_helper._is_packed_list(self):
            self = stack(g, self, g.op("Constant", value_t=torch.tensor([0])))
        return min(g, self)
    return min(g, self, other)
