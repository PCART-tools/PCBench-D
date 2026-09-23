@_onnx_symbolic("aten::normal")
def normal(
    g: jit_utils.GraphContext,
    mean,
    std,
    sizes=None,
    generator=None,
    dtype=None,
    layout=None,
    device=None,
    pin_memory=None,
):
    # If you can sample from a given distribution with mean 0 and variance 1, then you can easily sample from a
    # scale-location transformation of that distribution, which has mean mu and variance sigma's square. If x is a sample
    # from a mean 0 and variance 1 distribution then
    #       sigma x+mu
    # is a sample with mean mu and variance sigma's square.
    if sizes is not None and not symbolic_helper._is_none(sizes):
        mean = opset9.expand(g, mean, sizes, None)
    result = opset9.mul(g, std, g.op("RandomNormalLike", mean))
    return add(g, result, mean)
