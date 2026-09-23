@register_inference_rule(torch.nn.functional.layer_norm)
def layer_norm_functional(n: Node, symbols, constraints, counter):
    """
    We generate the constraint: input = output
    """
    assert isinstance(n.args[0], Node)
    return gen_layer_norm_constraints(n, n.args[1], symbols, counter)
