def relu6(g, input):
    relu = g.op("Relu", input)
    return clamp_max(g, relu, 6)
