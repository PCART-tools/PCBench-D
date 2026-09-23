def size(g, self, dim=None):
    if dim is None:
        return g.op("Shape", self)
    if sym_help._maybe_get_const(dim, "i") < 0:
        rank = sym_help._get_tensor_rank(self)
        if rank is not None:
            dim = sym_help._maybe_get_const(dim, "i") + rank
            dim = g.op("Constant", value_t=torch.tensor(dim))
    return sym_help._size_helper(g, self, dim)
