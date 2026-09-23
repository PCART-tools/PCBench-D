def _get_control_flow_submodules(
    graph_module: torch.fx.GraphModule,
) -> list[tuple[str, torch.nn.Module, torch.fx.Node]]:
    """
    Returns a list of submodules used for control flow operations
    (torch.ops.higher_order.cond/map) that are in the given toplevel graph (does not look
    into submodules). Specifically, the returned value is a list containing a
    tuple of (name of the submodule that's stored in the graph module, the
    submodule itself, and the fx node that uses this submodule).
    """
    control_flow_submodules = []
    for node in graph_module.graph.nodes:
        if node.op != "call_function":
            continue

        if node.target is torch.ops.higher_order.cond:
            control_flow_submodules.append(_get_submodule(graph_module, node, 1))
            control_flow_submodules.append(_get_submodule(graph_module, node, 2))
        if node.target is torch.ops.higher_order.map_impl:
            control_flow_submodules.append(_get_submodule(graph_module, node, 0))

    return control_flow_submodules
