def _make_graph_module(*args, graph_module_cls=None, **kwargs):
    if graph_module_cls is None:
        graph_module_cls = _get_graph_module_cls()

    return graph_module_cls(*args, **kwargs)
