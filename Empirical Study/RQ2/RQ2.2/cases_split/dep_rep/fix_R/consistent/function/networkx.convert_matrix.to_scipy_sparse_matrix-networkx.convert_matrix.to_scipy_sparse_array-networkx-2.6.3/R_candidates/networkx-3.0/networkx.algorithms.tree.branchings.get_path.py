def get_path(G, u, v):
    """
    Returns the edge keys of the unique path between u and v.

    This is not a generic function. G must be a branching and an instance of
    MultiDiGraph_EdgeKey.

    """
    nodes = nx.shortest_path(G, u, v)

    # We are guaranteed that there is only one edge connected every node
    # in the shortest path.

    def first_key(i, vv):
        # Needed for 2.x/3.x compatibilitity
        keys = G[nodes[i]][vv].keys()
        # Normalize behavior
        keys = list(keys)
        return keys[0]

    edges = [first_key(i, vv) for i, vv in enumerate(nodes[1:])]
    return nodes, edges
