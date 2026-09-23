def _replace_with_hop(node: torch.fx.Node) -> None:
    assert node.op == "call_module"
    graph: torch.fx.Graph = node.graph
    assert graph.owning_module is not None
    gm: torch.fx.GraphModule = graph.owning_module
    assert isinstance(node.target, str)
    sub_gm = getattr(gm, node.target)
    sub_graph = sub_gm.graph
    autocast_nodes = nodes_filter(sub_graph.nodes, _is_autocast_node)
    if len(autocast_nodes) > 0:
        assert len(autocast_nodes) > 1  # need at least an enter node and an exist node
        enter_autocast_node = autocast_nodes[0]
        exit_autocast_node = autocast_nodes[-1]
        _check_valid_autocast_block(enter_autocast_node, exit_autocast_node)

        _replace_with_hop_helper(node, enter_autocast_node, wrap_with_autocast)
        sub_graph.erase_node(exit_autocast_node)
        sub_graph.erase_node(enter_autocast_node)
