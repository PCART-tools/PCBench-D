@run_const_graph.py_impl(FakeTensorMode)
def run_const_graph_fake_tensor_mode(mode, graph, args):
    assert isinstance(graph, torch.fx.GraphModule)
    with mode:
        return graph(*args)
