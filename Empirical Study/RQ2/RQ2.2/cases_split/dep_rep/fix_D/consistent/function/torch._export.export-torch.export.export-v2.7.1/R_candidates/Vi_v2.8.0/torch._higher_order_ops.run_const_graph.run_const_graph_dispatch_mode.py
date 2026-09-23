@run_const_graph.py_impl(ProxyTorchDispatchMode)
def run_const_graph_dispatch_mode(mode, graph, args):
    const_gm, weights = graph, args
    p_args = pytree.tree_map(mode.tracer.unwrap_proxy, (graph, args))
    assert isinstance(const_gm, torch.fx.GraphModule)
    assert not hasattr(mode.tracer.root, "_const_graph")
    mode.tracer.root.register_module("_const_graph", const_gm)

    proxy = mode.tracer.create_proxy("call_function", run_const_graph, p_args, {})

    out = const_gm(*weights)
    return track_tensor_tree(out, proxy, constant=None, tracer=mode.tracer)
