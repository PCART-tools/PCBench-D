def prim_min(g, self, other=None):
    if not other:
        if (sym_help._is_packed_list(self)):
            self = stack(g, self, g.op("Constant", value_t=torch.tensor([0])))
        return min(g, self)
    return min(g, self, other)
