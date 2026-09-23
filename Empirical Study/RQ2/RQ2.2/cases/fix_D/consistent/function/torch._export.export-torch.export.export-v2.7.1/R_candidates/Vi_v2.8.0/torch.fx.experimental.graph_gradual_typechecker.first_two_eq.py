@register_refinement_rule(torch.nn.AdaptiveAvgPool2d)
@register_refinement_rule(torch.nn.MaxPool2d)
def first_two_eq(n: Node):
    """
    For operations where the first two dimensions of the input and output shape
    are equal
    """
    res = []
    assert isinstance(n.args[0], Node)
    arg_type = n.args[0].type
    if isinstance(arg_type, TensorType) and isinstance(n.type, TensorType):
        args1 = arg_type.__args__
        args2 = n.type.__args__
        res = [Equality(args1[0], args2[0]), Equality(args1[1], args2[1])]
    return res
