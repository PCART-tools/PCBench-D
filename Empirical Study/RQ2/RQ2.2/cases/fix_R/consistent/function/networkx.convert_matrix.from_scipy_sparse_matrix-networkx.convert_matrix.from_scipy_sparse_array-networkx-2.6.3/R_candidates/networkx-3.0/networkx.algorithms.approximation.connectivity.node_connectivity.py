def node_connectivity(G, s=None, t=None):
    r"""Returns an approximation for node connectivity for a graph or digraph G.

    Node connectivity is equal to the minimum number of nodes that
    must be removed to disconnect G or render it trivial. By Menger's theorem,
    this is equal to the number of node independent paths (paths that
    share no nodes other than source and target).

    If source and target nodes are provided, this function returns the
    local node connectivity: the minimum number of nodes that must be
    removed to break all paths from source to target in G.

    This algorithm is based on a fast approximation that gives an strict lower
    bound on the actual number of node independent paths between two nodes [1]_.
    It works for both directed and undirected graphs.

    Parameters
    ----------
    G : NetworkX graph
        Undirected graph

    s : node
        Source node. Optional. Default value: None.

    t : node
        Target node. Optional. Default value: None.

    Returns
    -------
    K : integer
        Node connectivity of G, or local node connectivity if source
        and target are provided.

    Examples
    --------
    >>> # Platonic octahedral graph is 4-node-connected
    >>> from networkx.algorithms import approximation as approx
    >>> G = nx.octahedral_graph()
    >>> approx.node_connectivity(G)
    4

    Notes
    -----
    This algorithm [1]_ finds node independents paths between two nodes by
    computing their shortest path using BFS, marking the nodes of the path
    found as 'used' and then searching other shortest paths excluding the
    nodes marked as used until no more paths exist. It is not exact because
    a shortest path could use nodes that, if the path were longer, may belong
    to two different node independent paths. Thus it only guarantees an
    strict lower bound on node connectivity.

    See also
    --------
    all_pairs_node_connectivity
    local_node_connectivity

    References
    ----------
    .. [1] White, Douglas R., and Mark Newman. 2001 A Fast Algorithm for
        Node-Independent Paths. Santa Fe Institute Working Paper #01-07-035
        http://eclectic.ss.uci.edu/~drwhite/working.pdf

    """
    if (s is not None and t is None) or (s is None and t is not None):
        raise nx.NetworkXError("Both source and target must be specified.")

    # Local node connectivity
    if s is not None and t is not None:
        if s not in G:
            raise nx.NetworkXError(f"node {s} not in graph")
        if t not in G:
            raise nx.NetworkXError(f"node {t} not in graph")
        return local_node_connectivity(G, s, t)

    # Global node connectivity
    if G.is_directed():
        connected_func = nx.is_weakly_connected
        iter_func = itertools.permutations

        def neighbors(v):
            return itertools.chain(G.predecessors(v), G.successors(v))

    else:
        connected_func = nx.is_connected
        iter_func = itertools.combinations
        neighbors = G.neighbors

    if not connected_func(G):
        return 0

    # Choose a node with minimum degree
    v, minimum_degree = min(G.degree(), key=itemgetter(1))
    # Node connectivity is bounded by minimum degree
    K = minimum_degree
    # compute local node connectivity with all non-neighbors nodes
    # and store the minimum
    for w in set(G) - set(neighbors(v)) - {v}:
        K = min(K, local_node_connectivity(G, v, w, cutoff=K))
    # Same for non adjacent pairs of neighbors of v
    for x, y in iter_func(neighbors(v), 2):
        if y not in G[x] and x != y:
            K = min(K, local_node_connectivity(G, x, y, cutoff=K))
    return K
