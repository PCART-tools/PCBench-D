@register_inference_rule(torch.nn.Linear)
def linear_inference_rule(n: Node, module_instance, symbols, constraints, counter):
    """
    Input and output sizes should be the same except for the last dimension
    If the input is Dyn, then so should the output
    """
    assert isinstance(n.args[0], Node)
    return linear_constraints(
        n, module_instance.in_features, module_instance.out_features, symbols, counter
    )
