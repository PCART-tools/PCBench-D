def intersection(G, H):
    """Returns a new graph that contains only the nodes and the edges that exist in
    both G and H.

    Parameters
    ----------
    G,H : graph
       A NetworkX graph. G and H can have different node sets but must be both graphs or both multigraphs.

    Raises
    ------
    NetworkXError
        If one is a MultiGraph and the other one is a graph.

    Returns
    -------
    GH : A new graph with the same type as G.

    Notes
    -----
    Attributes from the graph, nodes, and edges are not copied to the new
    graph.  If you want a new graph of the intersection of G and H
    with the attributes (including edge data) from G use remove_nodes_from()
    as follows

    >>> G = nx.path_graph(3)
    >>> H = nx.path_graph(5)
    >>> R = G.copy()
    >>> R.remove_nodes_from(n for n in G if n not in H)
    >>> R.remove_edges_from(e for e in G.edges if e not in H.edges)

    Examples
    --------
    >>> G = nx.Graph([(0, 1), (0, 2), (1, 2)])
    >>> H = nx.Graph([(0, 3), (1, 2), (2, 3)])
    >>> R = nx.intersection(G, H)
    >>> R.nodes
    NodeView((0, 1, 2))
    >>> R.edges
    EdgeView([(1, 2)])
    """
    return nx.intersection_all([G, H])
