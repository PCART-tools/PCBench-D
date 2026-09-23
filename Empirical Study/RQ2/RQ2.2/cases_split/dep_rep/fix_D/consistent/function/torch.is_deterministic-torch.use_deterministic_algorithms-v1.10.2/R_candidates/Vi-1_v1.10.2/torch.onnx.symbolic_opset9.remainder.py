def remainder(g, input, other):
    div = g.op("Div", input, other)
    if sym_help._is_fp(input) or sym_help._is_fp(other):
        div = g.op("Floor", div)
    quo = g.op("Mul", div, other)
    return g.op("Sub", input, quo)
