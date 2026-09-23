def __derive_index(g, index, start, step):
    return g.op("Add", start, g.op("Mul", index, step))
