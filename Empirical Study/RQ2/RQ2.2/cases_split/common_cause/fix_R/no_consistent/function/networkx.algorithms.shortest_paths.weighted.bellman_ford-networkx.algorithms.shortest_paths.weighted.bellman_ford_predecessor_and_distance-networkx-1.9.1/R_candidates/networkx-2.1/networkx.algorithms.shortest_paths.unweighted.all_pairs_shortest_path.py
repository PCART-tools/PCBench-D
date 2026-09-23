def all_pairs_shortest_path(G, cutoff=None):
    """Compute shortest paths between all nodes.

    Parameters
    ----------
    G : NetworkX graph

    cutoff : integer, optional
        Depth at which to stop the search. Only paths of length at most
        `cutoff` are returned.

    Returns
    -------
    lengths : dictionary
        Dictionary, keyed by source and target, of shortest paths.

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> path = dict(nx.all_pairs_shortest_path(G))
    >>> print(path[0][4])
    [0, 1, 2, 3, 4]

    See Also
    --------
    floyd_warshall()

    """
    # TODO This can be trivially parallelized.
    for n in G:
        yield (n, single_source_shortest_path(G, n, cutoff=cutoff))
