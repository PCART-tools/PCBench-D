def nets_to_graph_def(nets, shapes=None, **kwargs):
    '''
    Convert a set of Caffe2 nets to a Tensorflow graph.

    Args:
        nets: List of core.Nets. core.Net is a wrapper around a NetDef protobuf.
            The corresponding protobuf can be extracted using .Proto().
        shapes: Dictionary mapping blob names to their shapes/dimensions.

    Returns:
        Call to protos_to_graph_def() with the extracted NetDef protobufs and
            **kwargs. See _operators_to_graph_def for detailed **kwargs.
    '''
    # if shapes is None:
    #     shapes = _try_get_shapes(nets)
    # _try_get_shapes(nets) depends on workspace.InferShapesAndTypes(nets),
    # which is currently broken (segfault). We omit the shapes for now.
    shapes = {}
    nets = [copy.deepcopy(net.Proto()) for net in nets]
    shapes = copy.deepcopy(shapes)
    return protos_to_graph_def(nets, shapes, **kwargs)
