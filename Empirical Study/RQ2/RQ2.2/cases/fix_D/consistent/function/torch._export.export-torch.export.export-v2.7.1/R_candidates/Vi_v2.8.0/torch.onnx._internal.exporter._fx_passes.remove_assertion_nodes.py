def remove_assertion_nodes(graph_module: torch.fx.GraphModule) -> torch.fx.GraphModule:
    """Remove all assertion and check nodes from the FX graph"""
    aten_assertion_targets = {
        torch.ops.aten.sym_constrain_range_for_size.default,
        torch.ops.aten._assert_async.default,
        torch.ops.aten._assert_async.msg,
        torch.ops.aten._assert_scalar.default,
        torch.ops.aten._assert_tensor_metadata.default,
    }
    for node in graph_module.graph.nodes:
        if node.op == "call_function" and node.target in aten_assertion_targets:
            graph_module.graph.erase_node(node)
    graph_module.recompile()
    return graph_module
