@parse_args("v", "is", "i")
def frobenius_norm(g, self, dim=None, keepdim=False):
    sqr = g.op("Mul", self, self)
    sumsqr = sym_help._reducesum_helper(g, sqr, axes_i=dim, keepdims_i=keepdim)
    return g.op("Sqrt", sumsqr)
