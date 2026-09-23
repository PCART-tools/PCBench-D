def _extract_graph_module_outputs(graph_module: torch.fx.GraphModule) -> Any:
    """Collect "val" fields from outputs metadata in this torch.fx.GraphModule."""
    for node in graph_module.graph.nodes:
        if node.op == "output":
            # Output node is unique. Let's retrieve output values from
            # this node's input list. And then just return.
            return node.args[0]
    raise ValueError("No output node found in this torch.fx.GraphModule.")
