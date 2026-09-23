def geometric_edges(G, radius, p=2):
    """Returns edge list of node pairs within `radius` of each other.

    Parameters
    ----------
    G : networkx graph
        The graph from which to generate the edge list. The nodes in `G` should
        have an attribute ``pos`` corresponding to the node position, which is
        used to compute the distance to other nodes.
    radius : scalar
        The distance threshold. Edges are included in the edge list if the
        distance between the two nodes is less than `radius`.
    p : scalar, default=2
        The `Minkowski distance metric
        <https://en.wikipedia.org/wiki/Minkowski_distance>`_ used to compute
        distances. The default value is 2, i.e. Euclidean distance.

    Returns
    -------
    edges : list
        List of edges whose distances are less than `radius`

    Notes
    -----
    Radius uses Minkowski distance metric `p`.
    If scipy is available, `scipy.spatial.cKDTree` is used to speed computation.

    Examples
    --------
    Create a graph with nodes that have a "pos" attribute representing 2D
    coordinates.

    >>> G = nx.Graph()
    >>> G.add_nodes_from([
    ...     (0, {"pos": (0, 0)}),
    ...     (1, {"pos": (3, 0)}),
    ...     (2, {"pos": (8, 0)}),
    ... ])
    >>> nx.geometric_edges(G, radius=1)
    []
    >>> nx.geometric_edges(G, radius=4)
    [(0, 1)]
    >>> nx.geometric_edges(G, radius=6)
    [(0, 1), (1, 2)]
    >>> nx.geometric_edges(G, radius=9)
    [(0, 1), (0, 2), (1, 2)]
    """
    # Input validation - every node must have a "pos" attribute
    for n, pos in G.nodes(data="pos"):
        if pos is None:
            raise nx.NetworkXError(
                f"All nodes in `G` must have a 'pos' attribute. Check node {n}"
            )

    # NOTE: See _geometric_edges for the actual implementation. The reason this
    # is split into two functions is to avoid the overhead of input validation
    # every time the function is called internally in one of the other
    # geometric generators
    return _geometric_edges(G, radius, p)
