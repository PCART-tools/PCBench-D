def size(g, self, dim=None):
    if dim is None:
        return g.op("Shape", self)
    return sym_help._size_helper(g, self, dim)
