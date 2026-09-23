def _is_any_annotated(nodes: list[Node]):
    """
    Given a list of nodes (that represents an operator pattern),
    check if any of the node is annotated, return True if any of the node
    is annotated, otherwise return False.
    """
    return any(_is_node_annotated(node) for node in nodes)
