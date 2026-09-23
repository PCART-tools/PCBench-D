def _remove_set_grad_and_inline(node: torch.fx.Node) -> None:
    assert node.op == "call_module"
    graph: torch.fx.Graph = node.graph
    assert graph.owning_module is not None
    gm: torch.fx.GraphModule = graph.owning_module
    assert isinstance(node.target, str)
    sub_gm = getattr(gm, node.target)
    sub_graph = sub_gm.graph
    nodes_map(
        sub_graph.nodes,
        lambda n: sub_graph.erase_node(n) if _is_set_grad_enabled_node(n) else n,
    )
    node_inline_(node)
