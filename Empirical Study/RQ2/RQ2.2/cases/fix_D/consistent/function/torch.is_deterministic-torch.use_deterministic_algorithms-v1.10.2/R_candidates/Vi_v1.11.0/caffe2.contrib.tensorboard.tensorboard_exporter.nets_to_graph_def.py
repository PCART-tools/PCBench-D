def nets_to_graph_def(nets, shapes=None, **kwargs):
    if shapes is None:
        shapes = _try_get_shapes(nets)
    nets = [copy.deepcopy(net.Proto()) for net in nets]
    shapes = copy.deepcopy(shapes)
    for net in nets:
        _propagate_device_option(net)
    return _operators_to_graph_def(
        shapes,
        [op for net in nets for op in net.op],
        **kwargs
    )
