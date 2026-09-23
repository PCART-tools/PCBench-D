@register_inference_rule(getattr)
def get_attr_inference_rule(n: Node, traced):
    """
    The current getattr rule only handles the shape attribute
    Can be extended to other attributes
    The most representitive type we have is "Dyn" but the system
    can be extended with more types, such as a type to represent shapes
    """
    attr_node = n.args[0]
    attr_name = n.args[1]

    if attr_name == "shape":
        n.type = Dyn
    else:
        raise TypeError("Not yet implelemted")

    # TODO. We leave it like this till we add a type to represent tensor sizes
    return n.type
