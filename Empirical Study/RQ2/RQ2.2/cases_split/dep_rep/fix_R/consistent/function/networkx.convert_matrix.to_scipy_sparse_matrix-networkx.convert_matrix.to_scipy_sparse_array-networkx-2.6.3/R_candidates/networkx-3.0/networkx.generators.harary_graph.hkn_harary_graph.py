def hkn_harary_graph(k, n, create_using=None):
    """Returns the Harary graph with given node connectivity and node number.

    The Harary graph $H_{k,n}$ is the graph that minimizes the number of
    edges needed with given node connectivity $k$ and node number $n$.

    This smallest number of edges is known to be ceil($kn/2$) [1]_.

    Parameters
    ----------
    k: integer
       The node connectivity of the generated graph

    n: integer
       The number of nodes the generated graph is to contain

    create_using : NetworkX graph constructor, optional Graph type
     to create (default=nx.Graph). If graph instance, then cleared
     before populated.

    Returns
    -------
    NetworkX graph
        The Harary graph $H_{k,n}$.

    See Also
    --------
    hnm_harary_graph

    Notes
    -----
    This algorithm runs in $O(kn)$ time.
    It is implemented by following the Reference [2]_.

    References
    ----------
    .. [1] Weisstein, Eric W. "Harary Graph." From MathWorld--A Wolfram Web
     Resource. http://mathworld.wolfram.com/HararyGraph.html.

    .. [2] Harary, F. "The Maximum Connectivity of a Graph."
      Proc. Nat. Acad. Sci. USA 48, 1142-1146, 1962.
    """

    if k < 1:
        raise NetworkXError("The node connectivity must be >= 1!")
    if n < k + 1:
        raise NetworkXError("The number of nodes must be >= k+1 !")

    # in case of connectivity 1, simply return the path graph
    if k == 1:
        H = nx.path_graph(n, create_using)
        return H

    # Construct an empty graph with n nodes first
    H = nx.empty_graph(n, create_using)

    # Test the parity of k and n
    if (k % 2 == 0) or (n % 2 == 0):
        # Construct a regular graph with k degrees
        offset = k // 2
        for i in range(n):
            for j in range(1, offset + 1):
                H.add_edge(i, (i - j) % n)
                H.add_edge(i, (i + j) % n)
        if k & 1:
            # odd degree; n must be even in this case
            half = n // 2
            for i in range(0, half):
                # add edges diagonally
                H.add_edge(i, i + half)
    else:
        # Construct a regular graph with (k - 1) degrees
        offset = (k - 1) // 2
        for i in range(n):
            for j in range(1, offset + 1):
                H.add_edge(i, (i - j) % n)
                H.add_edge(i, (i + j) % n)
        half = n // 2
        for i in range(0, half + 1):
            # add half+1 edges between i and i+half
            H.add_edge(i, (i + half) % n)

    return H
