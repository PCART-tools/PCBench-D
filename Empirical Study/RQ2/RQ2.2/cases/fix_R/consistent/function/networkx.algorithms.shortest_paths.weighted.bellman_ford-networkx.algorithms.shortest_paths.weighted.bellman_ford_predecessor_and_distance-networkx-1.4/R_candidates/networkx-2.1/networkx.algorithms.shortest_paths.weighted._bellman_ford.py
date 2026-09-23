def _bellman_ford(G, source, weight, pred=None, paths=None, dist=None,
                  cutoff=None, target=None):
    """Relaxation loop for Bellman–Ford algorithm

    Parameters
    ----------
    G : NetworkX graph

    source: list
        List of source nodes

    weight : function
       The weight of an edge is the value returned by the function. The
       function must accept exactly three positional arguments: the two
       endpoints of an edge and the dictionary of edge attributes for
       that edge. The function must return a number.

    pred: dict of lists, optional (default=None)
        dict to store a list of predecessors keyed by that node
        If None, predecessors are not stored

    paths: dict, optional (default=None)
        dict to store the path list from source to each node, keyed by node
        If None, paths are not stored

    dist: dict, optional (default=None)
        dict to store distance from source to the keyed node
        If None, returned dist dict contents default to 0 for every node in the
        source list

    cutoff: integer or float, optional
        Depth to stop the search. Only paths of length <= cutoff are returned

    target: node label, optional
        Ending node for path. Path lengths to other destinations may (and
        probably will) be incorrect.

    Returns
    -------
    Returns a dict keyed by node to the distance from the source.
    Dicts for paths and pred are in the mutated input dicts by those names.

    Raises
    ------
    NetworkXUnbounded
       If the (di)graph contains a negative cost (di)cycle, the
       algorithm raises an exception to indicate the presence of the
       negative cost (di)cycle.  Note: any negative weight edge in an
       undirected graph is a negative cost cycle
    """

    if pred is None:
        pred = {v: [None] for v in source}

    if dist is None:
        dist = {v: 0 for v in source}

    G_succ = G.succ if G.is_directed() else G.adj
    inf = float('inf')
    n = len(G)

    count = {}
    q = deque(source)
    in_q = set(source)
    while q:
        u = q.popleft()
        in_q.remove(u)

        # Skip relaxations if any of the predecessors of u is in the queue.
        if all(pred_u not in in_q for pred_u in pred[u]):
            dist_u = dist[u]
            for v, e in G_succ[u].items():
                dist_v = dist_u + weight(v, u, e)

                if cutoff is not None:
                    if dist_v > cutoff:
                        continue

                if target is not None:
                    if dist_v > dist.get(target, inf):
                        continue

                if dist_v < dist.get(v, inf):
                    if v not in in_q:
                        q.append(v)
                        in_q.add(v)
                        count_v = count.get(v, 0) + 1
                        if count_v == n:
                            raise nx.NetworkXUnbounded(
                                "Negative cost cycle detected.")
                        count[v] = count_v
                    dist[v] = dist_v
                    pred[v] = [u]

                elif dist.get(v) is not None and dist_v == dist.get(v):
                    pred[v].append(u)

    if paths is not None:
        dsts = [target] if target is not None else pred
        for dst in dsts:

            path = [dst]
            cur = dst

            while pred[cur][0] is not None:
                cur = pred[cur][0]
                path.append(cur)

            path.reverse()
            paths[dst] = path

    return dist
