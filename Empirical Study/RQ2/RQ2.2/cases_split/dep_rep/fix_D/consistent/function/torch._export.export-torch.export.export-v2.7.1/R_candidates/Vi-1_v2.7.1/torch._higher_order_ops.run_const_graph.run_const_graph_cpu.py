@run_const_graph.py_impl(DispatchKey.CPU)
def run_const_graph_cpu(graph, args):
    assert isinstance(graph, torch.fx.GraphModule)
    return graph(*args)
