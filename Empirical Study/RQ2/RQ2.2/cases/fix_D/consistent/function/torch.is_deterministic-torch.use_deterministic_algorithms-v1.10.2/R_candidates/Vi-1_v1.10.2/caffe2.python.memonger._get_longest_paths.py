def _get_longest_paths(g, source_nodes):
    ''' Get the longest path for nodes in 'source_nodes'
        Find with bellman_ford() by setting weight = -1
    '''

    ng = copy.deepcopy(g)
    for u, v in ng.edges():
        ng[u][v]["weight"] = -1

    ret = {}
    for cn in source_nodes:
        pred, dist = nx.bellman_ford_predecessor_and_distance(ng, cn, weight="weight")
        path = _get_path(pred, dist)
        assert path[0] == cn
        assert len(path) - 1 == -dist[path[-1]]
        ret[cn] = path

    return ret
