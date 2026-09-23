@register_inference_rule("type_as")
def type_inference_rule(n: Node, symbols, constraints, counter):
    """
    We generate the constraint: input = output
    """
    assert isinstance(n.args[0], Node)
    assert isinstance(n.args[1], Node)

    output, counter = gen_tvar(counter)
    symbols[n] = output

    from_arg = symbols[n.args[0]]
    to_arg = symbols[n.args[1]]

    assert isinstance(from_arg, TVar)
    assert isinstance(to_arg, TVar)

    return [
        BinConstraintT(from_arg, to_arg, op_consistency),
        BinConstraintT(output, to_arg, op_eq),
    ], counter
