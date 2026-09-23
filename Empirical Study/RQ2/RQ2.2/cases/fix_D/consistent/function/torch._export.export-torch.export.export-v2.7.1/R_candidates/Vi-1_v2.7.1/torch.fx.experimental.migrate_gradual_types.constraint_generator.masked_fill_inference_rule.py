@register_inference_rule("masked_fill_")
def masked_fill_inference_rule(n: Node, symbols, constraints, counter):
    """
    Similar to addition. For now we implement the constraints when
    the argument is a boolean tensor. There is also a case for when
    it is a condition. We will leave this out for now.
    """

    assert isinstance(n.args[0], Node)
    assert isinstance(n.args[1], Node)

    # We will retrieve the type variables from the symbol table
    # and confirm they are tensor variables

    e1 = symbols[n.args[0]]
    e2 = symbols[n.args[1]]

    if isinstance(e1, TVar) and isinstance(e2, TVar):
        masked_fill_tensor, counter = gen_tvar(counter)
        symbols[n] = masked_fill_tensor
        return gen_broadcasting_constraints(
            e1, e2, symbols, counter, masked_fill_tensor
        )
    else:
        raise NotImplementedError("Not yet implemented")
