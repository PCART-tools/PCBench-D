def _replace_with_hop(node: torch.fx.Node) -> None:
    assert node.op == "call_module"
    graph: torch.fx.Graph = node.graph
    assert graph.owning_module is not None
    gm: torch.fx.GraphModule = graph.owning_module
    assert isinstance(node.target, str)
    sub_gm = getattr(gm, node.target)
    sub_graph = sub_gm.graph
    set_grad_nodes = nodes_filter(sub_graph.nodes, _is_set_grad_enabled_node)
    if len(set_grad_nodes) > 0:
        assert len(set_grad_nodes) == 1
        set_grad_node = set_grad_nodes[0]
        _replace_with_hop_helper(node, set_grad_node, wrap_with_set_grad_enabled)
        sub_graph.erase_node(set_grad_node)
