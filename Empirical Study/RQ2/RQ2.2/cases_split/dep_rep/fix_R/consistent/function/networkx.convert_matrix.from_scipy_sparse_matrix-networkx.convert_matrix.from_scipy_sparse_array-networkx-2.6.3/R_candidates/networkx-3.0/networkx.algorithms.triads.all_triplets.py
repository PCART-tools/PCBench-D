@not_implemented_for("undirected")
def all_triplets(G):
    """Returns a generator of all possible sets of 3 nodes in a DiGraph.

    Parameters
    ----------
    G : digraph
       A NetworkX DiGraph

    Returns
    -------
    triplets : generator of 3-tuples
       Generator of tuples of 3 nodes

    Examples
    --------
    >>> G = nx.DiGraph([(1, 2), (2, 3), (3, 4)])
    >>> list(nx.all_triplets(G))
    [(1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]

    """
    triplets = combinations(G.nodes(), 3)
    return triplets
