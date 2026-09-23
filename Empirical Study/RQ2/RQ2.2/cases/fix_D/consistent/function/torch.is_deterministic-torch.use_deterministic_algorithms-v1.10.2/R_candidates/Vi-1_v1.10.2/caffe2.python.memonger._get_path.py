def _get_path(pred_list, dist_list):
    ''' Get the path from nx.bellman_ford()'s output '''

    # distances are negative
    assert all(dist_list[x] <= 0 for x in dist_list)
    # node with longest distance to source is the target
    target = min(dist_list, key=lambda x: dist_list[x])

    ret = []
    cur = target

    while cur is not None:
        ret.append(cur)
        # Hack to get networkx 2.0 happy: it uses list in pred.
        # TODO(tulloch): are there cases with multiple predecessors?
        try:
            cur = pred_list[cur][0] if pred_list[cur] else None
        except TypeError:
            cur = pred_list[cur]

    return list(reversed(ret))
