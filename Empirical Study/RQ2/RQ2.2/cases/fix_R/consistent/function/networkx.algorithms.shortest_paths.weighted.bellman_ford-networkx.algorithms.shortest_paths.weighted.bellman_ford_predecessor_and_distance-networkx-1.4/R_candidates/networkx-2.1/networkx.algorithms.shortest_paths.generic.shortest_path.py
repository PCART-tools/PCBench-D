def shortest_path(G, source=None, target=None, weight=None):
    """Compute shortest paths in the graph.

    Parameters
    ----------
    G : NetworkX graph

    source : node, optional
        Starting node for path. If not specified, compute shortest
        paths for each possible starting node.

    target : node, optional
        Ending node for path. If not specified, compute shortest
        paths to all possible nodes.

    weight : None or string, optional (default = None)
        If None, every edge has weight/distance/cost 1.
        If a string, use this edge attribute as the edge weight.
        Any edge attribute not present defaults to 1.

    Returns
    -------
    path: list or dictionary
        All returned paths include both the source and target in the path.

        If the source and target are both specified, return a single list
        of nodes in a shortest path from the source to the target.

        If only the source is specified, return a dictionary keyed by
        targets with a list of nodes in a shortest path from the source
        to one of the targets.

        If only the target is specified, return a dictionary keyed by
        sources with a list of nodes in a shortest path from one of the
        sources to the target.

        If neither the source nor target are specified return a dictionary
        of dictionaries with path[source][target]=[list of nodes in path].

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> print(nx.shortest_path(G, source=0, target=4))
    [0, 1, 2, 3, 4]
    >>> p = nx.shortest_path(G, source=0) # target not specified
    >>> p[4]
    [0, 1, 2, 3, 4]
    >>> p = nx.shortest_path(G, target=4) # source not specified
    >>> p[0]
    [0, 1, 2, 3, 4]
    >>> p = nx.shortest_path(G) # source, target not specified
    >>> p[0][4]
    [0, 1, 2, 3, 4]

    Notes
    -----
    There may be more than one shortest path between a source and target.
    This returns only one of them.

    See Also
    --------
    all_pairs_shortest_path()
    all_pairs_dijkstra_path()
    single_source_shortest_path()
    single_source_dijkstra_path()
    """
    if source is None:
        if target is None:
            # Find paths between all pairs.
            if weight is None:
                paths = dict(nx.all_pairs_shortest_path(G))
            else:
                paths = dict(nx.all_pairs_dijkstra_path(G, weight=weight))
        else:
            # Find paths from all nodes co-accessible to the target.
            with nx.utils.reversed(G):
                if weight is None:
                    paths = nx.single_source_shortest_path(G, target)
                else:
                    paths = nx.single_source_dijkstra_path(G, target,
                                                           weight=weight)
                # Now flip the paths so they go from a source to the target.
                for target in paths:
                    paths[target] = list(reversed(paths[target]))

    else:
        if target is None:
            # Find paths to all nodes accessible from the source.
            if weight is None:
                paths = nx.single_source_shortest_path(G, source)
            else:
                paths = nx.single_source_dijkstra_path(G, source,
                                                       weight=weight)
        else:
            # Find shortest source-target path.
            if weight is None:
                paths = nx.bidirectional_shortest_path(G, source, target)
            else:
                paths = nx.dijkstra_path(G, source, target, weight)

    return paths
