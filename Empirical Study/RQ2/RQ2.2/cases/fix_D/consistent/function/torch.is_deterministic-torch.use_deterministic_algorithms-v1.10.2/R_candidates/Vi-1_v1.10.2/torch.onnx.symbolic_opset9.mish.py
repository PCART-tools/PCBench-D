def mish(g, input):
    return g.op('Mul', input, g.op('Tanh', g.op('Softplus', input)))
