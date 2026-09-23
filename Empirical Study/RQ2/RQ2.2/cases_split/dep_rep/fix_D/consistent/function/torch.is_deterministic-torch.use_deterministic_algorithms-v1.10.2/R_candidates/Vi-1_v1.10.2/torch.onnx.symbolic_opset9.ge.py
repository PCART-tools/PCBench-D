@wrap_logical_op_with_negation
def ge(g, input, other):
    return lt_impl(g, input, other)
