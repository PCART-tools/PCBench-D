@register_inference_rule("transpose")
def transpose_inference_rule(n: Node, symbols, constraints, counter):
    """
    Can be considered as a sequence of two index selects, so we generate constraints accordingly
    """
    assert isinstance(n.args[0], Node)
    assert isinstance(n.args[1], int)
    assert isinstance(n.args[2], int)

    output, counter = gen_tvar(counter)
    symbols[n] = output

    from_arg = symbols[n.args[0]]
    assert isinstance(from_arg, TVar)

    # input and output are dyn
    is_dyn = Conj(
        [BinConstraintT(from_arg, Dyn, op_eq), BinConstraintT(output, Dyn, op_eq)]
    )

    # or input is a tensor and we actually do the replacement
    c3 = Disj(
        [
            Transpose(i + 1, from_arg, n.args[1], n.args[2], output)
            for i in range(MAX_TENSOR_RANK)
        ]
    )

    return [Disj([is_dyn, c3])], counter
