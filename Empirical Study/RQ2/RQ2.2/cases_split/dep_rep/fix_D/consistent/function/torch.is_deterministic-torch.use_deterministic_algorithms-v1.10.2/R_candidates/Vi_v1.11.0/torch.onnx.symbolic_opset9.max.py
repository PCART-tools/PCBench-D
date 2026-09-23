def max(g, self, dim_or_y=None, keepdim=None):
    # torch.max(input)
    if dim_or_y is None and keepdim is None:
        return g.op("ReduceMax", self, keepdims_i=0)
    # torch.max(input, other)
    if keepdim is None:
        return g.op("Max", self, dim_or_y)
    # torch.max(input, dim, keepdim)
    else:
        dim = sym_help._get_const(dim_or_y, "i", "dim")
        keepdim = sym_help._get_const(keepdim, "i", "keepdim")
        max = g.op("ReduceMax", self, axes_i=[dim], keepdims_i=keepdim)
        indices = g.op("ArgMax", self, axis_i=dim, keepdims_i=keepdim)
        return max, indices
