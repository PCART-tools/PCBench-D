def _path_to_cycle(path):
    """
    Removes the edges from path that occur even number of times.
    Returns a set of edges
    """
    edges = set()
    for edge in pairwise(path):
        # Toggle whether to keep the current edge.
        edges ^= {edge}
    return edges
