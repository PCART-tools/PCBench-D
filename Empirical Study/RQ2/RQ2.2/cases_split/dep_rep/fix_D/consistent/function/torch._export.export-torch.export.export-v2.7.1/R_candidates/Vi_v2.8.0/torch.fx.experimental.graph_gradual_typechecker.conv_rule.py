@register_algebraic_expressions_inference_rule(Conv2d)
def conv_rule(n: Node, module_instance):
    """
    Represents the outout in terms of an algrbraic expression w.r.t
    the input when possible
    """
    assert isinstance(n.args[0], Node)
    arg_type = n.args[0].type
    if isinstance(arg_type, TensorType) and isinstance(n.type, TensorType):
        w_in = arg_type.__args__[3]
        h_in = arg_type.__args__[2]
        h_out = calculate_out_dimension(h_in, module_instance, 0)
        w_out = calculate_out_dimension(w_in, module_instance, 1)
        new_type = TensorType((n.type.__args__[0], n.type.__args__[1], h_out, w_out))
        n.type = new_type
        return new_type
