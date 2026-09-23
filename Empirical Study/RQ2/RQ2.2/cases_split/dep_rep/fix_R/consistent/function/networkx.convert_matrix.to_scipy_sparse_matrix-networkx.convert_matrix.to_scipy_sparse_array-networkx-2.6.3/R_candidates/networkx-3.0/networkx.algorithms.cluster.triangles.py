@nx._dispatch("triangles")
@not_implemented_for("directed")
def triangles(G, nodes=None):
    """Compute the number of triangles.

    Finds the number of triangles that include a node as one vertex.

    Parameters
    ----------
    G : graph
       A networkx graph
    nodes : container of nodes, optional (default= all nodes in G)
       Compute triangles for nodes in this container.

    Returns
    -------
    out : dictionary
       Number of triangles keyed by node label.

    Examples
    --------
    >>> G = nx.complete_graph(5)
    >>> print(nx.triangles(G, 0))
    6
    >>> print(nx.triangles(G))
    {0: 6, 1: 6, 2: 6, 3: 6, 4: 6}
    >>> print(list(nx.triangles(G, (0, 1)).values()))
    [6, 6]

    Notes
    -----
    When computing triangles for the entire graph each triangle is counted
    three times, once at each node.  Self loops are ignored.

    """
    # If `nodes` represents a single node in the graph, return only its number
    # of triangles.
    if nodes in G:
        return next(_triangles_and_degree_iter(G, nodes))[2] // 2
    # Otherwise, `nodes` represents an iterable of nodes, so return a
    # dictionary mapping node to number of triangles.
    return {v: t // 2 for v, d, t, _ in _triangles_and_degree_iter(G, nodes)}
