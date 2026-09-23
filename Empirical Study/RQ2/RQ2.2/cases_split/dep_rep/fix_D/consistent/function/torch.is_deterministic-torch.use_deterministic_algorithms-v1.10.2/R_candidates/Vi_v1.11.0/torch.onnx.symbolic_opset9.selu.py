def selu(g, input):
    return g.op("Selu", input)
