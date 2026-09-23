def hypercube_graph(n):
    """Returns the *n*-dimensional hypercube graph.

    The nodes are the integers between 0 and ``2 ** n - 1``, inclusive.

    For more information on the hypercube graph, see the Wikipedia
    article `Hypercube graph`_.

    .. _Hypercube graph: https://en.wikipedia.org/wiki/Hypercube_graph

    Parameters
    ----------
    n : int
        The dimension of the hypercube.
        The number of nodes in the graph will be ``2 ** n``.

    Returns
    -------
    NetworkX graph
        The hypercube graph of dimension *n*.
    """
    dim = n * [2]
    G = grid_graph(dim)
    return G
