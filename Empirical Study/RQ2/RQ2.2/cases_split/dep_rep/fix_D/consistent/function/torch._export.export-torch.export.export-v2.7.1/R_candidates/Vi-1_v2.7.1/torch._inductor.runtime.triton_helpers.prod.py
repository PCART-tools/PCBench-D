@triton.jit
def prod(input, axis):
    return tl.reduce(input, axis, _prod_accumulate)
