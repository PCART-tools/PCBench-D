@wrap_logical_op_with_cast_to_and_from("Bool")
def logical_xor(g, input, other):
    return g.op("Xor", input, other)
