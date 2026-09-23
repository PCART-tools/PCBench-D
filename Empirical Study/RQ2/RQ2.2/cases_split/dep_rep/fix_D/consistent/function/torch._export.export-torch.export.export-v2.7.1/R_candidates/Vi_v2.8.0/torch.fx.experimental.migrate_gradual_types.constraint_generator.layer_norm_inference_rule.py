@register_inference_rule(torch.nn.LayerNorm)
def layer_norm_inference_rule(n: Node, module_instance, symbols, constraints, counter):
    """
    Input and output shapes should be equal.
    Input should be consistent with the normalized_shape
    """
    assert isinstance(n.args[0], Node)
    return gen_layer_norm_constraints(
        n, module_instance.normalized_shape, symbols, counter
    )
