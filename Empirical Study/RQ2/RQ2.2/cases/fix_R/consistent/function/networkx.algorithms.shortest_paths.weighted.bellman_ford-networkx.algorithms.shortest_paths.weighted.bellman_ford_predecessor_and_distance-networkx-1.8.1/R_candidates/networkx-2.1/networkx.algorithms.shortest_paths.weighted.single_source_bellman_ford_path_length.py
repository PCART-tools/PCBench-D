def single_source_bellman_ford_path_length(G, source,
                                           cutoff=None, weight='weight'):
    """Compute the shortest path length between source and all other
    reachable nodes for a weighted graph.

    Parameters
    ----------
    G : NetworkX graph

    source : node label
       Starting node for path

    weight: string, optional (default='weight')
       Edge data key corresponding to the edge weight.

    cutoff : integer or float, optional
       Depth to stop the search. Only paths of length <= cutoff are returned.

    Returns
    -------
    length : iterator
        (target, shortest path length) iterator

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> length = dict(nx.single_source_bellman_ford_path_length(G, 0))
    >>> length[4]
    4
    >>> for node in [0, 1, 2, 3, 4]:
    ...     print('{}: {}'.format(node, length[node]))
    0: 0
    1: 1
    2: 2
    3: 3
    4: 4

    Notes
    -----
    Edge weight attributes must be numerical.
    Distances are calculated as sums of weighted edges traversed.

    See Also
    --------
    single_source_dijkstra(), single_source_bellman_ford()

    """
    weight = _weight_function(G, weight)
    return _bellman_ford(G, [source], weight, cutoff=cutoff)
