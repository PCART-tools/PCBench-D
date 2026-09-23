@parse_args("v")
def hardswish(g, self):
    hs = hardsigmoid(g, self)
    return g.op("Mul", self, hs)
