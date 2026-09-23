@not_implemented_for("directed")
def resistance_distance(G, nodeA, nodeB, weight=None, invert_weight=True):
    """Returns the resistance distance between node A and node B on graph G.

    The resistance distance between two nodes of a graph is akin to treating
    the graph as a grid of resistorses with a resistance equal to the provided
    weight.

    If weight is not provided, then a weight of 1 is used for all edges.

    Parameters
    ----------
    G : NetworkX graph
       A graph

    nodeA : node
      A node within graph G.

    nodeB : node
      A node within graph G, exclusive of Node A.

    weight : string or None, optional (default=None)
       The edge data key used to compute the resistance distance.
       If None, then each edge has weight 1.

    invert_weight : boolean (default=True)
        Proper calculation of resistance distance requires building the
        Laplacian matrix with the reciprocal of the weight. Not required
        if the weight is already inverted. Weight cannot be zero.

    Returns
    -------
    rd : float
       Value of effective resistance distance

    Examples
    --------
    >>> G = nx.Graph([(1, 2), (1, 3), (1, 4), (3, 4), (3, 5), (4, 5)])
    >>> nx.resistance_distance(G, 1, 3)
    0.625

    Notes
    -----
    Overviews are provided in [1]_ and [2]_. Additional details on computational
    methods, proofs of properties, and corresponding MATLAB codes are provided
    in [3]_.

    References
    ----------
    .. [1] Wikipedia
       "Resistance distance."
       https://en.wikipedia.org/wiki/Resistance_distance
    .. [2] E. W. Weisstein
       "Resistance Distance."
       MathWorld--A Wolfram Web Resource
       https://mathworld.wolfram.com/ResistanceDistance.html
    .. [3] V. S. S. Vos,
       "Methods for determining the effective resistance."
       Mestrado, Mathematisch Instituut Universiteit Leiden, 2016
       https://www.universiteitleiden.nl/binaries/content/assets/science/mi/scripties/master/vos_vaya_master.pdf
    """
    import numpy as np
    import scipy as sp
    import scipy.sparse.linalg  # call as sp.sparse.linalg

    if not nx.is_connected(G):
        msg = "Graph G must be strongly connected."
        raise nx.NetworkXError(msg)
    elif nodeA not in G:
        msg = "Node A is not in graph G."
        raise nx.NetworkXError(msg)
    elif nodeB not in G:
        msg = "Node B is not in graph G."
        raise nx.NetworkXError(msg)
    elif nodeA == nodeB:
        msg = "Node A and Node B cannot be the same."
        raise nx.NetworkXError(msg)

    G = G.copy()
    node_list = list(G)

    if invert_weight and weight is not None:
        if G.is_multigraph():
            for (u, v, k, d) in G.edges(keys=True, data=True):
                d[weight] = 1 / d[weight]
        else:
            for (u, v, d) in G.edges(data=True):
                d[weight] = 1 / d[weight]
    # Replace with collapsing topology or approximated zero?

    # Using determinants to compute the effective resistance is more memory
    # efficient than directly calculating the psuedo-inverse
    L = nx.laplacian_matrix(G, node_list, weight=weight).asformat("csc")
    indices = list(range(L.shape[0]))
    # w/ nodeA removed
    indices.remove(node_list.index(nodeA))
    L_a = L[indices, :][:, indices]
    # Both nodeA and nodeB removed
    indices.remove(node_list.index(nodeB))
    L_ab = L[indices, :][:, indices]

    # Factorize Laplacian submatrixes and extract diagonals
    # Order the diagonals to minimize the likelihood over overflows
    # during computing the determinant
    lu_a = sp.sparse.linalg.splu(L_a, options=dict(SymmetricMode=True))
    LdiagA = lu_a.U.diagonal()
    LdiagA_s = np.product(np.sign(LdiagA)) * np.product(lu_a.L.diagonal())
    LdiagA_s *= (-1) ** _count_lu_permutations(lu_a.perm_r)
    LdiagA_s *= (-1) ** _count_lu_permutations(lu_a.perm_c)
    LdiagA = np.absolute(LdiagA)
    LdiagA = np.sort(LdiagA)

    lu_ab = sp.sparse.linalg.splu(L_ab, options=dict(SymmetricMode=True))
    LdiagAB = lu_ab.U.diagonal()
    LdiagAB_s = np.product(np.sign(LdiagAB)) * np.product(lu_ab.L.diagonal())
    LdiagAB_s *= (-1) ** _count_lu_permutations(lu_ab.perm_r)
    LdiagAB_s *= (-1) ** _count_lu_permutations(lu_ab.perm_c)
    LdiagAB = np.absolute(LdiagAB)
    LdiagAB = np.sort(LdiagAB)

    # Calculate the ratio of determinant, rd = det(L_ab)/det(L_a)
    Ldet = np.product(np.divide(np.append(LdiagAB, [1]), LdiagA))
    rd = Ldet * LdiagAB_s / LdiagA_s

    return rd
