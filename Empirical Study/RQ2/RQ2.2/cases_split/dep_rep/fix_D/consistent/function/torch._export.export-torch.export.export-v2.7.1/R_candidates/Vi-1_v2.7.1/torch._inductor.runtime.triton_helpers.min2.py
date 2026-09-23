@triton.jit
def min2(a, dim):
    return tl.reduce(a, dim, minimum)
