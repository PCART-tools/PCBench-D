@register_inference_rule(torch.nn.Linear)
def linear_inference_rule(n: Node, module_instance):
    """
    Applies the shape information to the input then gets the greatest upper bound
    of the resulting type and the existing type
    """
    assert isinstance(n.args[0], Node)
    if n.args[0].type == Dyn and isinstance(n.type, TensorType):
        n.args[0].type = expand_to_tensor_dim(n.args[0].type, len(n.type.__args__))
    if isinstance(n.args[0].type, TensorType):
        output_type = linear_check(n.args[0].type, module_instance)
        n.type = get_greatest_upper_bound(output_type, n.type)
    return n.type
