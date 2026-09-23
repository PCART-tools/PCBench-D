def havel_hakimi_graph(deg_sequence, create_using=None):
    """Returns a simple graph with given degree sequence constructed
    using the Havel-Hakimi algorithm.

    Parameters
    ----------
    deg_sequence: list of integers
        Each integer corresponds to the degree of a node (need not be sorted).
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
        Graph type to create. If graph instance, then cleared before populated.
        Directed graphs are not allowed.

    Raises
    ------
    NetworkXException
        For a non-graphical degree sequence (i.e. one
        not realizable by some simple graph).

    Notes
    -----
    The Havel-Hakimi algorithm constructs a simple graph by
    successively connecting the node of highest degree to other nodes
    of highest degree, resorting remaining nodes by degree, and
    repeating the process. The resulting graph has a high
    degree-associativity.  Nodes are labeled 1,.., len(deg_sequence),
    corresponding to their position in deg_sequence.

    The basic algorithm is from Hakimi [1]_ and was generalized by
    Kleitman and Wang [2]_.

    References
    ----------
    .. [1] Hakimi S., On Realizability of a Set of Integers as
       Degrees of the Vertices of a Linear Graph. I,
       Journal of SIAM, 10(3), pp. 496-506 (1962)
    .. [2] Kleitman D.J. and Wang D.L.
       Algorithms for Constructing Graphs and Digraphs with Given Valences
       and Factors  Discrete Mathematics, 6(1), pp. 79-88 (1973)
    """
    if not nx.is_graphical(deg_sequence):
        raise nx.NetworkXError("Invalid degree sequence")

    p = len(deg_sequence)
    G = nx.empty_graph(p, create_using)
    if G.is_directed():
        raise nx.NetworkXError("Directed graphs are not supported")
    num_degs = [[] for i in range(p)]
    dmax, dsum, n = 0, 0, 0
    for d in deg_sequence:
        # Process only the non-zero integers
        if d > 0:
            num_degs[d].append(n)
            dmax, dsum, n = max(dmax, d), dsum + d, n + 1
    # Return graph if no edges
    if n == 0:
        return G

    modstubs = [(0, 0)] * (dmax + 1)
    # Successively reduce degree sequence by removing the maximum degree
    while n > 0:
        # Retrieve the maximum degree in the sequence
        while len(num_degs[dmax]) == 0:
            dmax -= 1
        # If there are not enough stubs to connect to, then the sequence is
        # not graphical
        if dmax > n - 1:
            raise nx.NetworkXError("Non-graphical integer sequence")

        # Remove largest stub in list
        source = num_degs[dmax].pop()
        n -= 1
        # Reduce the next dmax largest stubs
        mslen = 0
        k = dmax
        for i in range(dmax):
            while len(num_degs[k]) == 0:
                k -= 1
            target = num_degs[k].pop()
            G.add_edge(source, target)
            n -= 1
            if k > 1:
                modstubs[mslen] = (k - 1, target)
                mslen += 1
        # Add back to the list any nonzero stubs that were removed
        for i in range(mslen):
            (stubval, stubtarget) = modstubs[i]
            num_degs[stubval].append(stubtarget)
            n += 1

    return G
