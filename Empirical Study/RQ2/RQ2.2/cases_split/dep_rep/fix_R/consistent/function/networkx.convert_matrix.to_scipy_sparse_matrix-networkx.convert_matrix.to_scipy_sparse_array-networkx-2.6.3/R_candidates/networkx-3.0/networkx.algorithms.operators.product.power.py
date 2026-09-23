@not_implemented_for("directed")
@not_implemented_for("multigraph")
def power(G, k):
    """Returns the specified power of a graph.

    The $k$th power of a simple graph $G$, denoted $G^k$, is a
    graph on the same set of nodes in which two distinct nodes $u$ and
    $v$ are adjacent in $G^k$ if and only if the shortest path
    distance between $u$ and $v$ in $G$ is at most $k$.

    Parameters
    ----------
    G : graph
        A NetworkX simple graph object.

    k : positive integer
        The power to which to raise the graph `G`.

    Returns
    -------
    NetworkX simple graph
        `G` to the power `k`.

    Raises
    ------
    ValueError
        If the exponent `k` is not positive.

    NetworkXNotImplemented
        If `G` is not a simple graph.

    Examples
    --------
    The number of edges will never decrease when taking successive
    powers:

    >>> G = nx.path_graph(4)
    >>> list(nx.power(G, 2).edges)
    [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
    >>> list(nx.power(G, 3).edges)
    [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

    The `k`th power of a cycle graph on *n* nodes is the complete graph
    on *n* nodes, if `k` is at least ``n // 2``:

    >>> G = nx.cycle_graph(5)
    >>> H = nx.complete_graph(5)
    >>> nx.is_isomorphic(nx.power(G, 2), H)
    True
    >>> G = nx.cycle_graph(8)
    >>> H = nx.complete_graph(8)
    >>> nx.is_isomorphic(nx.power(G, 4), H)
    True

    References
    ----------
    .. [1] J. A. Bondy, U. S. R. Murty, *Graph Theory*. Springer, 2008.

    Notes
    -----
    This definition of "power graph" comes from Exercise 3.1.6 of
    *Graph Theory* by Bondy and Murty [1]_.

    """
    if k <= 0:
        raise ValueError("k must be a positive integer")
    H = nx.Graph()
    H.add_nodes_from(G)
    # update BFS code to ignore self loops.
    for n in G:
        seen = {}  # level (number of hops) when seen in BFS
        level = 1  # the current level
        nextlevel = G[n]
        while nextlevel:
            thislevel = nextlevel  # advance to next level
            nextlevel = {}  # and start a new list (fringe)
            for v in thislevel:
                if v == n:  # avoid self loop
                    continue
                if v not in seen:
                    seen[v] = level  # set the level of vertex v
                    nextlevel.update(G[v])  # add neighbors of v
            if k <= level:
                break
            level += 1
        H.add_edges_from((n, nbr) for nbr in seen)
    return H
