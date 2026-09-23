def ops_to_graph_def(ops, shapes=None, **kwargs):
    ops = copy.deepcopy(ops)
    shapes = copy.deepcopy(shapes or {})
    return _operators_to_graph_def(shapes, ops, **kwargs)
