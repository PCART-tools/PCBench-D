@register_inference_rule(torch.nn.functional.gelu)
@register_inference_rule(torch.nn.functional.dropout)
@register_inference_rule(torch.nn.functional.softmax)
@register_inference_rule("detach")
@register_inference_rule("to")
@register_inference_rule("int")
@register_inference_rule("long")
@register_inference_rule("contiguous")
@register_inference_rule(torch.ones)
@register_inference_rule(torch.zeros)
def equality_inference_rule(n: Node, symbols, constraints, counter):
    """
    We generate the constraint: input = output
    """
    output, counter = gen_tvar(counter)
    symbols[n] = output

    if isinstance(n.args[0], Node):
        input = symbols[n.args[0]]
        if isinstance(input, TVar):
            return [BinConstraintT(input, output, op_eq)], counter

        # then we have dimension variables
        else:
            for arg in n.args:
                assert isinstance(symbols[arg], DVar)
        my_size = [symbols[arg] for arg in n.args]
        return [BinConstraintT(output, TensorType(my_size), op_eq)], counter

    elif isinstance(n.args[0], tuple):
        # then the tuple is the size
        assert len(n.args[0]) <= 4
        my_size = [symbols[arg] for arg in n.args[0]]
        return [BinConstraintT(output, TensorType(my_size), op_eq)], counter
    else:
        raise NotImplementedError("Method not yet implemented")
