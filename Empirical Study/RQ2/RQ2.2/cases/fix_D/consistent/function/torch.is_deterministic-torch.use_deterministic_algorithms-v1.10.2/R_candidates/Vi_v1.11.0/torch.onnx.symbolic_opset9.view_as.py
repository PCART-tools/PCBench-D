def view_as(g, self, other):
    shape = g.op("Shape", other)
    return reshape(g, self, shape)
