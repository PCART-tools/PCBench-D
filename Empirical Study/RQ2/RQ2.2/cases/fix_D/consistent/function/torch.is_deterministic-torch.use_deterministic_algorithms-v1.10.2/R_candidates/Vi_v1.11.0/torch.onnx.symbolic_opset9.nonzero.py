@parse_args("v")
def nonzero(g, input):
    return t(g, g.op("NonZero", input))
