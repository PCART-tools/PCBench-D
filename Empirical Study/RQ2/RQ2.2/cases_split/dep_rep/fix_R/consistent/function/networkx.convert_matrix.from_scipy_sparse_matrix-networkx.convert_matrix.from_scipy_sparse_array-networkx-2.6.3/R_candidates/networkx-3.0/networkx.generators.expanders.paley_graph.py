def paley_graph(p, create_using=None):
    """Returns the Paley (p-1)/2-regular graph on p nodes.

    The returned graph is a graph on Z/pZ with edges between x and y
    if and only if x-y is a nonzero square in Z/pZ.

    If p = 1 mod 4, -1 is a square in Z/pZ and therefore x-y is a square if and
    only if y-x is also a square, i.e the edges in the Paley graph are symmetric.

    If p = 3 mod 4, -1 is not a square in Z/pZ and therefore either x-y or y-x
    is a square in Z/pZ but not both.

    Note that a more general definition of Paley graphs extends this construction
    to graphs over q=p^n vertices, by using the finite field F_q instead of Z/pZ.
    This construction requires to compute squares in general finite fields and is
    not what is implemented here (i.e paley_graph(25) does not return the true
    Paley graph associated with 5^2).

    Parameters
    ----------
    p : int, an odd prime number.

    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : graph
        The constructed directed graph.

    Raises
    ------
    NetworkXError
        If the graph is a multigraph.

    References
    ----------
    Chapter 13 in B. Bollobas, Random Graphs. Second edition.
    Cambridge Studies in Advanced Mathematics, 73.
    Cambridge University Press, Cambridge (2001).
    """
    G = nx.empty_graph(0, create_using, default=nx.DiGraph)
    if G.is_multigraph():
        msg = "`create_using` cannot be a multigraph."
        raise nx.NetworkXError(msg)

    # Compute the squares in Z/pZ.
    # Make it a set to uniquify (there are exactly (p-1)/2 squares in Z/pZ
    # when is prime).
    square_set = {(x**2) % p for x in range(1, p) if (x**2) % p != 0}

    for x in range(p):
        for x2 in square_set:
            G.add_edge(x, (x + x2) % p)
    G.graph["name"] = f"paley({p})"
    return G
