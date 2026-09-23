def all_shortest_paths(G, source, target, weight=None):
    """Compute all shortest paths in the graph.

    Parameters
    ----------
    G : NetworkX graph

    source : node
       Starting node for path.

    target : node
       Ending node for path.

    weight : None or string, optional (default = None)
       If None, every edge has weight/distance/cost 1.
       If a string, use this edge attribute as the edge weight.
       Any edge attribute not present defaults to 1.

    Returns
    -------
    paths : generator of lists
        A generator of all paths between source and target.

    Examples
    --------
    >>> G = nx.Graph()
    >>> nx.add_path(G, [0, 1, 2])
    >>> nx.add_path(G, [0, 10, 2])
    >>> print([p for p in nx.all_shortest_paths(G, source=0, target=2)])
    [[0, 1, 2], [0, 10, 2]]

    Notes
    -----
    There may be many shortest paths between the source and target.

    See Also
    --------
    shortest_path()
    single_source_shortest_path()
    all_pairs_shortest_path()
    """
    if weight is not None:
        pred, dist = nx.dijkstra_predecessor_and_distance(G, source,
                                                          weight=weight)
    else:
        pred = nx.predecessor(G, source)

    if source not in G:
        raise nx.NodeNotFound('Source {} is not in G'.format(source))

    if target not in pred:
        raise nx.NetworkXNoPath()

    stack = [[target, 0]]
    top = 0
    while top >= 0:
        node, i = stack[top]
        if node == source:
            yield [p for p, n in reversed(stack[:top + 1])]
        if len(pred[node]) > i:
            top += 1
            if top == len(stack):
                stack.append([pred[node][i], 0])
            else:
                stack[top] = [pred[node][i], 0]
        else:
            stack[top - 1][1] += 1
            top -= 1
