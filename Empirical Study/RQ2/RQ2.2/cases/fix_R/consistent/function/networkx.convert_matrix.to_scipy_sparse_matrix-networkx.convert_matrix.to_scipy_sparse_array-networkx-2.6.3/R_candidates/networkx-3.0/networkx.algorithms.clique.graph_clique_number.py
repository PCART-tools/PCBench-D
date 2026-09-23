def graph_clique_number(G, cliques=None):
    """Returns the clique number of the graph.

    The *clique number* of a graph is the size of the largest clique in
    the graph.

    Parameters
    ----------
    G : NetworkX graph
        An undirected graph.

    cliques : list
        A list of cliques, each of which is itself a list of nodes. If
        not specified, the list of all cliques will be computed, as by
        :func:`find_cliques`.

    Returns
    -------
    int
        The size of the largest clique in `G`.

    Notes
    -----
    You should provide `cliques` if you have already computed the list
    of maximal cliques, in order to avoid an exponential time search for
    maximal cliques.

    """
    if len(G.nodes) < 1:
        return 0
    if cliques is None:
        cliques = find_cliques(G)
    return max([len(c) for c in cliques] or [1])
