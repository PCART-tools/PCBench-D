def min(g, self, dim_or_y=None, keepdim=None):
    # torch.min(input)
    if dim_or_y is None and keepdim is None:
        return g.op("ReduceMin", self, keepdims_i=0)
    # torch.min(input, other)
    if keepdim is None:
        return g.op("Min", self, dim_or_y)
    # torch.min(input, dim, keepdim)
    else:
        dim = sym_help._get_const(dim_or_y, "i", "dim")
        keepdim = sym_help._get_const(keepdim, "i", "keepdim")
        min = g.op("ReduceMin", self, axes_i=[dim], keepdims_i=keepdim)
        indices = g.op("ArgMin", self, axis_i=dim, keepdims_i=keepdim)
        return min, indices
