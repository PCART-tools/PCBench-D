def bfs_trace_with_node_process(
    model: Union[ExportedProgram, torch.fx.GraphModule], node_op: Callable
) -> None:
    """Traverse the graph module and apply node_op to each node."""

    assert isinstance(model, (ExportedProgram, torch.fx.GraphModule)), (
        f"Expected GraphModule or ExportedProgram, got {type(model)}"
    )
    gm = model.graph_module if isinstance(model, ExportedProgram) else model
    queue = [gm]
    while queue:
        current_graph_module = queue.pop(0)
        for node in current_graph_module.graph.nodes:
            if node.op in ["output", "placeholder"]:
                continue

            node_op(node)

        control_flow_submodules = [
            submodule
            for _, submodule, _ in _get_control_flow_submodules(current_graph_module)
        ]
        queue.extend(control_flow_submodules)
