def is_weakly_connected(graph: Graph) -> bool:
    """
    Return true iff graph is weakly connected.
    """
    if not graph:
        return True
    neighbors: List[Set[int]] = [set() for _ in graph]
    for node, predecessors in enumerate(graph):
        for pred in predecessors:
            neighbors[pred].add(node)
            neighbors[node].add(pred)
    # assume nonempty graph
    stack = [0]
    found = {0}
    while stack:
        node = stack.pop()
        for neighbor in neighbors[node]:
            if neighbor not in found:
                found.add(neighbor)
                stack.append(neighbor)
    return len(found) == len(graph)
