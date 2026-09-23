@wrap_logical_op_with_cast_to_and_from("Bool")
def __or_(g, input, other):
    return g.op("Or", input, other)
