@register_lowering(aten.unbind, type_promotion_kind=None)
def unbind(x, dim=0):
    dim = _validate_dim(x, dim, 0)
    x_size = V.graph.sizevars.evaluate_static_shape(x.get_size()[dim])
    result = [select(x, dim, i) for i in range(x_size)]
    return result
