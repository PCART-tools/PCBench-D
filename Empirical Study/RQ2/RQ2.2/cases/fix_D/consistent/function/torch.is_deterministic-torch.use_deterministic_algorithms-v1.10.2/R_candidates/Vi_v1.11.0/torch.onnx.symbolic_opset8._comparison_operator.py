def _comparison_operator(g, input, other, op_name):
    other = sym_help._maybe_get_scalar(other)
    other = sym_help._if_scalar_type_as(g, other, input)
    _, input, other = _try_cast_integer_to_float(g, input, other)
    return g.op(op_name, input, other)
