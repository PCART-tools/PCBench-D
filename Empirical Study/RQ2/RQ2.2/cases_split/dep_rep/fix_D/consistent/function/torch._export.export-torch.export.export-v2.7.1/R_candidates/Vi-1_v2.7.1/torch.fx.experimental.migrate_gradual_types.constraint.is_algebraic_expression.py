def is_algebraic_expression(constraint):
    if isinstance(constraint, BinConstraintD):
        return constraint.op in [op_add, op_sub, op_div, op_mul, op_mod]
    else:
        return isinstance(constraint, Prod)
