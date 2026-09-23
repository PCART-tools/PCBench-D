@triton.jit
def any(a, dim):
    return tl.reduce(a, dim, _any_combine)
