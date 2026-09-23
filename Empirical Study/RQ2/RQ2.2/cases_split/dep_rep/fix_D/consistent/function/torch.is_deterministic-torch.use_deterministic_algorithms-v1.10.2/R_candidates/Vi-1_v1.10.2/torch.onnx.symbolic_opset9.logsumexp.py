@parse_args("v", "is", "i")
def logsumexp(g, input, dim, keepdim):
    return g.op("ReduceLogSumExp", input, axes_i=dim, keepdims_i=keepdim)
