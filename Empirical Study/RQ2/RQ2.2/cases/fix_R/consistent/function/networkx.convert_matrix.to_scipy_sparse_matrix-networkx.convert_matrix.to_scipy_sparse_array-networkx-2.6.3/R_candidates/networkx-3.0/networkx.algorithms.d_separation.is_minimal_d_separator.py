@not_implemented_for("undirected")
def is_minimal_d_separator(G, u, v, z):
    """Determine if a d-separating set is minimal.

    A d-separating set, `z`, in a DAG is a set of nodes that blocks
    all paths between the two nodes, `u` and `v`. This function
    verifies that a set is "minimal", meaning there is no smaller
    d-separating set between the two nodes.

    Parameters
    ----------
    G : nx.DiGraph
        The graph.
    u : node
        A node in the graph.
    v : node
        A node in the graph.
    z : Set of nodes
        The set of nodes to check if it is a minimal d-separating set.

    Returns
    -------
    bool
        Whether or not the `z` separating set is minimal.

    Raises
    ------
    NetworkXError
        Raises a :exc:`NetworkXError` if the input graph is not a DAG.

    NodeNotFound
        If any of the input nodes are not found in the graph,
        a :exc:`NodeNotFound` exception is raised.

    References
    ----------
    .. [1] Tian, J., & Paz, A. (1998). Finding Minimal D-separators.

    Notes
    -----
    This function only works on verifying a d-separating set is minimal
    between two nodes. To verify that a d-separating set is minimal between
    two sets of nodes is not supported.

    Uses algorithm 2 presented in [1]_. The complexity of the algorithm
    is :math:`O(|E_{An}^m|)`, where :math:`|E_{An}^m|` stands for the
    number of edges in the moralized graph of the sub-graph consisting
    of only the ancestors of ``u`` and ``v``.

    The algorithm works by constructing the moral graph consisting of just
    the ancestors of `u` and `v`. First, it performs BFS on the moral graph
    starting from `u` and marking any nodes it encounters that are part of
    the separating set, `z`. If a node is marked, then it does not continue
    along that path. In the second stage, BFS with markings is repeated on the
    moral graph starting from `v`. If at any stage, any node in `z` is
    not marked, then `z` is considered not minimal. If the end of the algorithm
    is reached, then `z` is minimal.

    For full details, see [1]_.

    https://en.wikipedia.org/wiki/Bayesian_network#d-separation
    """
    if not nx.is_directed_acyclic_graph(G):
        raise nx.NetworkXError("graph should be directed acyclic")

    union_uv = {u, v}
    union_uv.update(z)

    if any(n not in G.nodes for n in union_uv):
        raise nx.NodeNotFound("one or more specified nodes not found in the graph")

    x_anc = nx.ancestors(G, u)
    y_anc = nx.ancestors(G, v)
    xy_anc = x_anc.union(y_anc)

    # if Z contains any node which is not in ancestors of X or Y
    # then it is definitely not minimal
    if any(node not in xy_anc for node in z):
        return False

    D_anc_xy = x_anc.union(y_anc)
    D_anc_xy.update((u, v))

    # second, construct the moralization of the subgraph
    moral_G = nx.moral_graph(G.subgraph(D_anc_xy))

    # start BFS from X
    marks = _bfs_with_marks(moral_G, u, z)

    # if not all the Z is marked, then the set is not minimal
    if any(node not in marks for node in z):
        return False

    # similarly, start BFS from Y and check the marks
    marks = _bfs_with_marks(moral_G, v, z)
    # if not all the Z is marked, then the set is not minimal
    if any(node not in marks for node in z):
        return False

    return True
