def join(G, u, v, theta, alpha, metric):
    """Returns ``True`` if and only if the nodes whose attributes are
    ``du`` and ``dv`` should be joined, according to the threshold
    condition for geographical threshold graphs.

    ``G`` is an undirected NetworkX graph, and ``u`` and ``v`` are nodes
    in that graph. The nodes must have node attributes ``'pos'`` and
    ``'weight'``.

    ``metric`` is a distance metric.

    """
    du, dv = G.nodes[u], G.nodes[v]
    u_pos, v_pos = du["pos"], dv["pos"]
    u_weight, v_weight = du["weight"], dv["weight"]
    return (u_weight + v_weight) * metric(u_pos, v_pos) ** alpha >= theta
