def normal(g, loc, scale, seed):
    # If you can sample from a given distribution with mean 0 and variance 1, then you can easily sample from a
    # scale-location transformation of that distribution, which has mean μ and variance σ's square. If x is a sample
    # from a mean 0 and variance 1 distribution then
    #       σx+μ
    # is a sample with mean μ and variance σ's square.
    result = mul(g, scale, g.op("RandomNormalLike", loc))
    return add(g, result, loc)
