@parse_args("v", "i", "v")
def select(g, self, dim, index):
    return g.op("Gather", self, index, axis_i=dim)
