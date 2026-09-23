@register_inference_rule(torch.nn.ReLU)
def relu_inference_rule(n: Node, module_instance):
    """
    Input and output shapes should be equal.
    """
    assert isinstance(n.args[0], Node)

    if n.args[0].type == Dyn and isinstance(n.type, TensorType):
        n.args[0].type = expand_to_tensor_dim(n.args[0].type, len(n.type.__args__))

    if isinstance(n.args[0].type, TensorType):
        n.type = get_greatest_upper_bound(n.args[0].type, n.type)
    return n.type
