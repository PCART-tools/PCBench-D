def insert(g, self, pos, tensor):
    return g.op("SequenceInsert", self, tensor, pos)
