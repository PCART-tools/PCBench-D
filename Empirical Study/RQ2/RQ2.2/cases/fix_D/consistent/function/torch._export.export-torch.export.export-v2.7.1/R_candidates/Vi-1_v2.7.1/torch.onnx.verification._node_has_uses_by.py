def _node_has_uses_by(node: torch.Node, nodes: Collection[torch.Node]) -> bool:
    for output in node.outputs():
        if _has_uses_by_nodes(output, nodes):
            return True
    return False
