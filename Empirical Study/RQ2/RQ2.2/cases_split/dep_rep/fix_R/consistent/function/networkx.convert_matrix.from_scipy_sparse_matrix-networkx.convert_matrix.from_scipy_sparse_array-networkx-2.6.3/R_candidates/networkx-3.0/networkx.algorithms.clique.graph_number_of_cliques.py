def graph_number_of_cliques(G, cliques=None):
    """Returns the number of maximal cliques in the graph.

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
        The number of maximal cliques in `G`.

    Notes
    -----
    You should provide `cliques` if you have already computed the list
    of maximal cliques, in order to avoid an exponential time search for
    maximal cliques.

    """
    if cliques is None:
        cliques = list(find_cliques(G))
    return len(cliques)
