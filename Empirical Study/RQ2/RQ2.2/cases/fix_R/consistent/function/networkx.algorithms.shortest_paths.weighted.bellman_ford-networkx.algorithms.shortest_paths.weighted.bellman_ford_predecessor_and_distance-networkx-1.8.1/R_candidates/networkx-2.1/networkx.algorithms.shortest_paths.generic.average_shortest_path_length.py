def average_shortest_path_length(G, weight=None):
    r"""Return the average shortest path length.

    The average shortest path length is

    .. math::

       a =\sum_{s,t \in V} \frac{d(s, t)}{n(n-1)}

    where `V` is the set of nodes in `G`,
    `d(s, t)` is the shortest path from `s` to `t`,
    and `n` is the number of nodes in `G`.

    Parameters
    ----------
    G : NetworkX graph

    weight : None or string, optional (default = None)
       If None, every edge has weight/distance/cost 1.
       If a string, use this edge attribute as the edge weight.
       Any edge attribute not present defaults to 1.

    Raises
    ------
    NetworkXPointlessConcept
        If `G` is the null graph (that is, the graph on zero nodes).

    NetworkXError
        If `G` is not connected (or not weakly connected, in the case
        of a directed graph).

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> nx.average_shortest_path_length(G)
    2.0

    For disconnected graphs, you can compute the average shortest path
    length for each component

    >>> G = nx.Graph([(1, 2), (3, 4)])
    >>> for C in nx.connected_component_subgraphs(G):
    ...     print(nx.average_shortest_path_length(C))
    1.0
    1.0

    """
    n = len(G)
    # For the special case of the null graph, raise an exception, since
    # there are no paths in the null graph.
    if n == 0:
        msg = ('the null graph has no paths, thus there is no average'
               'shortest path length')
        raise nx.NetworkXPointlessConcept(msg)
    # For the special case of the trivial graph, return zero immediately.
    if n == 1:
        return 0
    # Shortest path length is undefined if the graph is disconnected.
    if G.is_directed() and not nx.is_weakly_connected(G):
        raise nx.NetworkXError("Graph is not weakly connected.")
    if not G.is_directed() and not nx.is_connected(G):
        raise nx.NetworkXError("Graph is not connected.")
    # Compute all-pairs shortest paths.
    if weight is None:
        def path_length(v): return nx.single_source_shortest_path_length(G, v)
    else:
        ssdpl = nx.single_source_dijkstra_path_length

        def path_length(v): return ssdpl(G, v, weight=weight)
    # Sum the distances for each (ordered) pair of source and target node.
    s = sum(l for u in G for l in path_length(u).values())
    return s / (n * (n - 1))
