@compatibility(is_backward_compatible=False)
def _get_graph_module_cls():
    return _LazyGraphModule if _use_lazy_graph_module_flag else GraphModule
