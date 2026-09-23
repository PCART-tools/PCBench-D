def append(g, self, tensor):
    return g.op("SequenceInsert", self, tensor)
