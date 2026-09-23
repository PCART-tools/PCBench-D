@parse_args("v", "f", "f", "i", "none")
def rrelu(g, input, lower, upper, training, generator):
    p = g.op("RandomUniformLike", input, high_f=upper, low_f=lower)
    return g.op("PRelu", input, p)
