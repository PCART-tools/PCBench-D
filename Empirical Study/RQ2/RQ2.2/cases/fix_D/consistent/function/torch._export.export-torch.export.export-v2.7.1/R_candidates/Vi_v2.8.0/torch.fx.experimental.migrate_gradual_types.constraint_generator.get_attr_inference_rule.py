@register_inference_rule(getattr)
def get_attr_inference_rule(n: Node, symbols, constraints, counter):
    """
    If the attribute is "device" then the tensor shape is preserved
    """
    assert isinstance(n.args[0], Node)
    assert isinstance(n.args[1], str)
    output, counter = gen_tvar(counter)
    symbols[n] = output

    input = symbols[n.args[0]]
    attr = n.args[1]

    if attr == "device":
        return [BinConstraintT(input, output, op_eq)], counter
    else:
        raise NotImplementedError("Not yet implemented")
