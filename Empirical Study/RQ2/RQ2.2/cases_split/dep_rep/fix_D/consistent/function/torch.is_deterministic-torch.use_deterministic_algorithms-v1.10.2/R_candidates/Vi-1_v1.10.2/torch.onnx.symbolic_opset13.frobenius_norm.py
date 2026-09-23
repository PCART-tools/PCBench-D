@parse_args("v", "v", "i")
def frobenius_norm(g, self, dim=None, keepdim=False):
    dim_val = sym_help._maybe_get_const(dim, "is")
    if not sym_help._is_value(dim_val) and len(dim_val) == 0:
        return g.op("ReduceL2", self, keepdims_i=0)
    sqr = g.op("Mul", self, self)
    sumsqr = sym_help._reducesum_helper(g, sqr, dim, keepdims_i=keepdim)
    return g.op("Sqrt", sumsqr)
