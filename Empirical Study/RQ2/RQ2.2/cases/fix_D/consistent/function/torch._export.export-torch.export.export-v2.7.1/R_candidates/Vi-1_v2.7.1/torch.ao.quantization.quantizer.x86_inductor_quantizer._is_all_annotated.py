def _is_all_annotated(nodes: list[Node]):
    """
    Given a list of nodes (that represents an operator pattern),
    return True if all of the node is annotated, otherwise return False.
    """
    return all(_is_node_annotated(node) for node in nodes)
