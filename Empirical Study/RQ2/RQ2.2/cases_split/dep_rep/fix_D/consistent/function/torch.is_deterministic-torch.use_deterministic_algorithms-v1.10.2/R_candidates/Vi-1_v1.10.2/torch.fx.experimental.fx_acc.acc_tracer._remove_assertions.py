def _remove_assertions(gm: torch.fx.GraphModule) -> bool:
    """
    Unconditionally removes all assertions found in GraphModule gm.
    Returns whether the graph is modified.
    """
    changed = False
    for node in gm.graph.nodes:
        if node.op == "call_function" and node.target == torch._assert:
            gm.graph.erase_node(node)
            changed = True
    return changed
