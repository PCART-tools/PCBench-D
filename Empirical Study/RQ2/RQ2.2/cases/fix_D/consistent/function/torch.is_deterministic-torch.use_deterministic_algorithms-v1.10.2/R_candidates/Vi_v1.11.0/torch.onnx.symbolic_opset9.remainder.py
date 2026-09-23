def remainder(g, input, other):
    div = _floor_divide(g, input, other)
    quo = g.op("Mul", div, other)
    return g.op("Sub", input, quo)
