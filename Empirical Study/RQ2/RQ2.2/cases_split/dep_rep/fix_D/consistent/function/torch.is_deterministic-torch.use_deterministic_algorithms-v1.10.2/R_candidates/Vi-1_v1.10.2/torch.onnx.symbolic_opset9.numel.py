def numel(g, self):
    shape = g.op("Shape", self)
    return g.op("ReduceProd", shape, keepdims_i=0)
