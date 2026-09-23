@wrap_logical_op_with_negation
def le(g, input, other):
    return gt_impl(g, input, other)
