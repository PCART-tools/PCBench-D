def shortest_path_length(G, source=None, target=None, weight=None):
    """Compute shortest path lengths in the graph.

    Parameters
    ----------
    G : NetworkX graph

    source : node, optional
        Starting node for path.
        If not specified, compute shortest path lengths using all nodes as
        source nodes.

    target : node, optional
        Ending node for path.
        If not specified, compute shortest path lengths using all nodes as
        target nodes.

    weight : None or string, optional (default = None)
        If None, every edge has weight/distance/cost 1.
        If a string, use this edge attribute as the edge weight.
        Any edge attribute not present defaults to 1.

    Returns
    -------
    length: int or iterator
        If the source and target are both specified, return the length of
        the shortest path from the source to the target.

        If only the source is specified, return a dict keyed by target
        to the shortest path length from the source to that target.

        If only the target is specified, return a dict keyed by source
        to the shortest path length from that source to the target.

        If neither the source nor target are specified, return an iterator
        over (source, dictionary) where dictionary is keyed by target to
        shortest path length from source to that target.

    Raises
    ------
    NetworkXNoPath
        If no path exists between source and target.

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> nx.shortest_path_length(G, source=0, target=4)
    4
    >>> p = nx.shortest_path_length(G, source=0) # target not specified
    >>> p[4]
    4
    >>> p = nx.shortest_path_length(G, target=4) # source not specified
    >>> p[0]
    4
    >>> p = dict(nx.shortest_path_length(G)) # source,target not specified
    >>> p[0][4]
    4

    Notes
    -----
    The length of the path is always 1 less than the number of nodes involved
    in the path since the length measures the number of edges followed.

    For digraphs this returns the shortest directed path length. To find path
    lengths in the reverse direction use G.reverse(copy=False) first to flip
    the edge orientation.

    See Also
    --------
    all_pairs_shortest_path_length()
    all_pairs_dijkstra_path_length()
    single_source_shortest_path_length()
    single_source_dijkstra_path_length()

    """
    if source is None:
        if target is None:
            # Find paths between all pairs.
            if weight is None:
                paths = nx.all_pairs_shortest_path_length(G)
            else:
                paths = nx.all_pairs_dijkstra_path_length(G, weight=weight)
        else:
            # Find paths from all nodes co-accessible to the target.
            with nx.utils.reversed(G):
                if weight is None:
                    # We need to exhaust the iterator as Graph needs
                    # to be reversed.
                    path_length = nx.single_source_shortest_path_length
                    paths = path_length(G, target)
                else:
                    path_length = nx.single_source_dijkstra_path_length
                    paths = path_length(G, target, weight=weight)
    else:
        if source not in G:
            raise nx.NodeNotFound("Source {} not in G".format(source))

        if target is None:
            # Find paths to all nodes accessible from the source.
            if weight is None:
                paths = nx.single_source_shortest_path_length(G, source)
            else:
                paths = nx.single_source_dijkstra_path_length(G, source,
                                                              weight=weight)
        else:
            # Find shortest source-target path.
            if weight is None:
                p = nx.bidirectional_shortest_path(G, source, target)
                paths = len(p) - 1
            else:
                paths = nx.dijkstra_path_length(G, source, target, weight)
    return paths
