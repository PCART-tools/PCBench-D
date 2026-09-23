def wrap_logical_op_with_negation(func):
    def wrap_with_not(g, input, other):
        return g.op("Not", func(g, input, other))
    return wrap_with_not
