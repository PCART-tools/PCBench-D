@nx._dispatch
@not_implemented_for("directed")
@not_implemented_for("multigraph")
def k_truss(G, k):
    """Returns the k-truss of `G`.

    The k-truss is the maximal induced subgraph of `G` which contains at least
    three vertices where every edge is incident to at least `k-2` triangles.

    Parameters
    ----------
    G : NetworkX graph
      An undirected graph
    k : int
      The order of the truss

    Returns
    -------
    H : NetworkX graph
      The k-truss subgraph

    Raises
    ------
    NetworkXError

      The k-truss is not defined for graphs with self loops or parallel edges
      or directed graphs.

    Notes
    -----
    A k-clique is a (k-2)-truss and a k-truss is a (k+1)-core.

    Not implemented for digraphs or graphs with parallel edges or self loops.

    Graph, node, and edge attributes are copied to the subgraph.

    K-trusses were originally defined in [2] which states that the k-truss
    is the maximal induced subgraph where each edge belongs to at least
    `k-2` triangles. A more recent paper, [1], uses a slightly different
    definition requiring that each edge belong to at least `k` triangles.
    This implementation uses the original definition of `k-2` triangles.

    References
    ----------
    .. [1] Bounds and Algorithms for k-truss. Paul Burkhardt, Vance Faber,
       David G. Harris, 2018. https://arxiv.org/abs/1806.05523v2
    .. [2] Trusses: Cohesive Subgraphs for Social Network Analysis. Jonathan
       Cohen, 2005.
    """
    H = G.copy()

    n_dropped = 1
    while n_dropped > 0:
        n_dropped = 0
        to_drop = []
        seen = set()
        for u in H:
            nbrs_u = set(H[u])
            seen.add(u)
            new_nbrs = [v for v in nbrs_u if v not in seen]
            for v in new_nbrs:
                if len(nbrs_u & set(H[v])) < (k - 2):
                    to_drop.append((u, v))
        H.remove_edges_from(to_drop)
        n_dropped = len(to_drop)
        H.remove_nodes_from(list(nx.isolates(H)))

    return H
