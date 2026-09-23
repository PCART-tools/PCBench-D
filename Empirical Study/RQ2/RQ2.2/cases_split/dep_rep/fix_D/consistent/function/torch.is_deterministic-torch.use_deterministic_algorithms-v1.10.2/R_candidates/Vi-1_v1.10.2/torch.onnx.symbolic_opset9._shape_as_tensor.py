def _shape_as_tensor(g, input):
    return g.op("Shape", input)
