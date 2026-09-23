def _remove_exceptions(gm: torch.fx.GraphModule) -> bool:
    """
    Unconditionally removes all call_modules to ConditionalExceptionWrappers
    found in GraphModule gm. Returns whether the graph is modified.
    """
    changed = False
    for node in gm.graph.nodes:
        if node.op == "call_module" and isinstance(
            gm.get_submodule(node.target), ConditionalExceptionWrapper
        ):
            gm.graph.erase_node(node)
            changed = True
    return changed
