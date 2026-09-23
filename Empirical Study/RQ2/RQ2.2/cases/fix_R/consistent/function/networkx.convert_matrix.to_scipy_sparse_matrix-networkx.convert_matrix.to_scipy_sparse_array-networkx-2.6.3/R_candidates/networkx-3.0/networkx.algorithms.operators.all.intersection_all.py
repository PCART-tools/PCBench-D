def intersection_all(graphs):
    """Returns a new graph that contains only the nodes and the edges that exist in
    all graphs.

    Parameters
    ----------
    graphs : iterable
       Iterable of NetworkX graphs

    Returns
    -------
    R : A new graph with the same type as the first graph in list

    Raises
    ------
    ValueError
       If `graphs` is an empty list.

    Notes
    -----
    Attributes from the graph, nodes, and edges are not copied to the new
    graph.
    """
    R = None

    for i, G in enumerate(graphs):
        G_nodes_set = set(G.nodes)
        G_edges_set = set(G.edges(keys=True) if G.is_multigraph() else G.edges())
        if i == 0:
            # create new graph
            R = G.__class__()
            node_intersection = G_nodes_set
            edge_intersection = G_edges_set
        elif G.is_multigraph() != R.is_multigraph():
            raise nx.NetworkXError("All graphs must be graphs or multigraphs.")
        else:
            node_intersection &= G_nodes_set
            edge_intersection &= G_edges_set

        R.graph.update(G.graph)

    if R is None:
        raise ValueError("cannot apply intersection_all to an empty list")

    R.add_nodes_from(node_intersection)
    R.add_edges_from(edge_intersection)

    return R
