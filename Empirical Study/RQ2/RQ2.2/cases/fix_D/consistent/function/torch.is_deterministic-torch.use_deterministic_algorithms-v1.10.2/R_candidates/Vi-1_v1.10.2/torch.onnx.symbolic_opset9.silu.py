def silu(g, input):
    return g.op("Mul", input, g.op("Sigmoid", input))
