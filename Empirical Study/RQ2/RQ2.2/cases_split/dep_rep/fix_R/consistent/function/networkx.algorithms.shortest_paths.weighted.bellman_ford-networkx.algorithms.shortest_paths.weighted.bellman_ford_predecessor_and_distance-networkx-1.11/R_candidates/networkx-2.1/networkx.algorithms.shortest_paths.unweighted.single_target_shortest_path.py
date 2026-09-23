def single_target_shortest_path(G, target, cutoff=None):
    """Compute shortest path to target from all nodes that reach target.

    Parameters
    ----------
    G : NetworkX graph

    target : node label
       Target node for path

    cutoff : integer, optional
        Depth to stop the search. Only paths of length <= cutoff are returned.

    Returns
    -------
    lengths : dictionary
        Dictionary, keyed by target, of shortest paths.

    Examples
    --------
    >>> G = nx.path_graph(5, create_using=nx.DiGraph())
    >>> path = nx.single_target_shortest_path(G, 4)
    >>> path[0]
    [0, 1, 2, 3, 4]

    Notes
    -----
    The shortest path is not necessarily unique. So there can be multiple
    paths between the source and each target node, all of which have the
    same 'shortest' length. For each target node, this function returns
    only one of those paths.

    See Also
    --------
    shortest_path, single_source_shortest_path
    """
    if target not in G:
        raise nx.NodeNotFound("Target {} not in G".format(source))

    def join(p1, p2):
        return p2 + p1
    # handle undirected graphs
    adj = G.pred if G.is_directed() else G.adj
    if cutoff is None:
        cutoff = float('inf')
    nextlevel = {target: 1}     # list of nodes to check at next level
    paths = {target: [target]}  # paths dictionary  (paths to key from source)
    return dict(_single_shortest_path(adj, nextlevel, paths, cutoff, join))
