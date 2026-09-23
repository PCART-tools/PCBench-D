@wrap_logical_op_with_negation
def ne(g, self, other):
    return g.op("Equal", self, other)
