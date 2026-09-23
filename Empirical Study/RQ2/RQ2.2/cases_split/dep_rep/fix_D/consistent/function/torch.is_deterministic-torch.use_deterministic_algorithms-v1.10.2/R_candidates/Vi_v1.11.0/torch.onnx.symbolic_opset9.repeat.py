def repeat(g, self, repeats):
    dtype = ScalarType.INT64
    shape_ = ones_like(g, repeats, dtype)
    self = g.op("Expand", self, shape_)
    return g.op("Tile", self, repeats)
