@register_refinement_rule(BatchNorm2d)
@register_refinement_rule(torch.nn.ReLU)
def all_eq(n: Node):
    """
    For operations where the input shape is equal to the output shape
    """
    res = []
    assert isinstance(n.args[0], Node)
    arg_type = n.args[0].type
    if isinstance(arg_type, TensorType) and isinstance(n.type, TensorType):
        args1 = arg_type.__args__
        args2 = n.type.__args__
        res = [Equality(args1[i], args2[i]) for i in range(len(args1))]
    return res
