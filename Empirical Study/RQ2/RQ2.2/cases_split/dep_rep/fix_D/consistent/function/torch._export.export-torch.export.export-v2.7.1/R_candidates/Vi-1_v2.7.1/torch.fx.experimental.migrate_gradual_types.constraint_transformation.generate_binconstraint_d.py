@register_transformation_rule(BinConstraintD)
def generate_binconstraint_d(constraint, counter):
    """
    Transform binary constraints for dimensions
    """
    if constraint.op == op_precision:
        if isinstance(constraint.lhs, int):
            return BinConstraintD(constraint.lhs, constraint.rhs, op_eq), counter
        elif constraint.lhs == Dyn:
            return T(), counter

    elif constraint.op == op_consistency:
        return (
            Disj(
                [
                    BinConstraintD(constraint.lhs, constraint.rhs, op_eq),
                    BinConstraintD(constraint.rhs, Dyn, op_eq),
                    BinConstraintD(constraint.lhs, Dyn, op_eq),
                ]
            ),
            counter,
        )

    else:
        return constraint, counter
