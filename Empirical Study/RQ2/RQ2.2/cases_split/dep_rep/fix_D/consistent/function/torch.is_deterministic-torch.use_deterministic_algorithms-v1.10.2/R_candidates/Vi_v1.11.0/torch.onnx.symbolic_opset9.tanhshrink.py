@parse_args("v")
def tanhshrink(g, self):
    return g.op("Sub", self, tanh(g, self))
