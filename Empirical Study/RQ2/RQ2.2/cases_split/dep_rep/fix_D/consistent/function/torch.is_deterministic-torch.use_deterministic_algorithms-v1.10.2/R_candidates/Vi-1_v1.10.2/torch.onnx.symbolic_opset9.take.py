def take(g, self, index):
    self_flattened = sym_help._reshape_helper(g, self, g.op("Constant", value_t=torch.tensor([-1], dtype=torch.int64)))
    out = index_select(g, self_flattened, 0, index)
    out = reshape_as(g, out, index)
    return out
