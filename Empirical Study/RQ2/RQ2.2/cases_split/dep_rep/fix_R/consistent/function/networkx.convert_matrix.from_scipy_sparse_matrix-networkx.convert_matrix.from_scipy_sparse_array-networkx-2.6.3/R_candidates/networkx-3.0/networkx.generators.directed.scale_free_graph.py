@py_random_state(7)
def scale_free_graph(
    n,
    alpha=0.41,
    beta=0.54,
    gamma=0.05,
    delta_in=0.2,
    delta_out=0,
    create_using=None,
    seed=None,
    initial_graph=None,
):
    """Returns a scale-free directed graph.

    Parameters
    ----------
    n : integer
        Number of nodes in graph
    alpha : float
        Probability for adding a new node connected to an existing node
        chosen randomly according to the in-degree distribution.
    beta : float
        Probability for adding an edge between two existing nodes.
        One existing node is chosen randomly according the in-degree
        distribution and the other chosen randomly according to the out-degree
        distribution.
    gamma : float
        Probability for adding a new node connected to an existing node
        chosen randomly according to the out-degree distribution.
    delta_in : float
        Bias for choosing nodes from in-degree distribution.
    delta_out : float
        Bias for choosing nodes from out-degree distribution.
    create_using : NetworkX graph constructor, optional
        The default is a MultiDiGraph 3-cycle.
        If a graph instance, use it without clearing first.
        If a graph constructor, call it to construct an empty graph.

        .. deprecated:: 3.0

           create_using is deprecated, use `initial_graph` instead.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    initial_graph : MultiDiGraph instance, optional
        Build the scale-free graph starting from this initial MultiDiGraph,
        if provided.


    Returns
    -------
    MultiDiGraph

    Examples
    --------
    Create a scale-free graph on one hundred nodes::

    >>> G = nx.scale_free_graph(100)

    Notes
    -----
    The sum of `alpha`, `beta`, and `gamma` must be 1.

    References
    ----------
    .. [1] B. Bollobás, C. Borgs, J. Chayes, and O. Riordan,
           Directed scale-free graphs,
           Proceedings of the fourteenth annual ACM-SIAM Symposium on
           Discrete Algorithms, 132--139, 2003.
    """

    def _choose_node(candidates, node_list, delta):
        if delta > 0:
            bias_sum = len(node_list) * delta
            p_delta = bias_sum / (bias_sum + len(candidates))
            if seed.random() < p_delta:
                return seed.choice(node_list)
        return seed.choice(candidates)

    if create_using is not None:
        import warnings

        warnings.warn(
            "The create_using argument is deprecated and will be removed in the future.\n\n"
            "To create a scale free graph from an existing MultiDiGraph, use\n"
            "initial_graph instead.",
            DeprecationWarning,
            stacklevel=2,
        )

    # TODO: Rm all this complicated logic when deprecation expires and replace
    # with commented code:
    #    if initial_graph is not None and hasattr(initial_graph, "_adj"):
    #        G = initial_graph
    #    else:
    #        # Start with 3-cycle
    #        G = nx.MultiDiGraph([(0, 1), (1, 2), (2, 0)])
    if create_using is not None and hasattr(create_using, "_adj"):
        if initial_graph is not None:
            raise ValueError(
                "Cannot set both create_using and initial_graph. Set create_using=None."
            )
        G = create_using
    else:
        if initial_graph is not None and hasattr(initial_graph, "_adj"):
            G = initial_graph
        else:
            G = nx.MultiDiGraph([(0, 1), (1, 2), (2, 0)])
    if not (G.is_directed() and G.is_multigraph()):
        raise nx.NetworkXError("MultiDiGraph required in initial_graph")

    if alpha <= 0:
        raise ValueError("alpha must be > 0.")
    if beta <= 0:
        raise ValueError("beta must be > 0.")
    if gamma <= 0:
        raise ValueError("gamma must be > 0.")

    if abs(alpha + beta + gamma - 1.0) >= 1e-9:
        raise ValueError("alpha+beta+gamma must equal 1.")

    if delta_in < 0:
        raise ValueError("delta_in must be >= 0.")

    if delta_out < 0:
        raise ValueError("delta_out must be >= 0.")

    # pre-populate degree states
    vs = sum((count * [idx] for idx, count in G.out_degree()), [])
    ws = sum((count * [idx] for idx, count in G.in_degree()), [])

    # pre-populate node state
    node_list = list(G.nodes())

    # see if there already are number-based nodes
    numeric_nodes = [n for n in node_list if isinstance(n, numbers.Number)]
    if len(numeric_nodes) > 0:
        # set cursor for new nodes appropriately
        cursor = max(int(n.real) for n in numeric_nodes) + 1
    else:
        # or start at zero
        cursor = 0

    while len(G) < n:
        r = seed.random()

        # random choice in alpha,beta,gamma ranges
        if r < alpha:
            # alpha
            # add new node v
            v = cursor
            cursor += 1
            # also add to node state
            node_list.append(v)
            # choose w according to in-degree and delta_in
            w = _choose_node(ws, node_list, delta_in)

        elif r < alpha + beta:
            # beta
            # choose v according to out-degree and delta_out
            v = _choose_node(vs, node_list, delta_out)
            # choose w according to in-degree and delta_in
            w = _choose_node(ws, node_list, delta_in)

        else:
            # gamma
            # choose v according to out-degree and delta_out
            v = _choose_node(vs, node_list, delta_out)
            # add new node w
            w = cursor
            cursor += 1
            # also add to node state
            node_list.append(w)

        # add edge to graph
        G.add_edge(v, w)

        # update degree states
        vs.append(v)
        ws.append(w)

    return G
