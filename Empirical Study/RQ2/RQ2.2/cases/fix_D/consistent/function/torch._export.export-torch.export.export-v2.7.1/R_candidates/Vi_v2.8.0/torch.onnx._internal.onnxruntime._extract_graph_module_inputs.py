def _extract_graph_module_inputs(graph_module: torch.fx.GraphModule) -> tuple[Any, ...]:
    placeholders = []
    for node in graph_module.graph.nodes:
        if node.op == "placeholder":
            if hasattr(node, "meta") and "val" in node.meta:
                assert isinstance(node.meta["val"], torch.Tensor)
            placeholders.append(node)
    return tuple(placeholders)
