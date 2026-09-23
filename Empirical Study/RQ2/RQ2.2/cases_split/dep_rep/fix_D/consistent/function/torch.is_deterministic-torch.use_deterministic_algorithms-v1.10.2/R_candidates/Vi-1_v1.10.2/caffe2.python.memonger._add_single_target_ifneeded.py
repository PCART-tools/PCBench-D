def _add_single_target_ifneeded(g):
    targets = _find_target_nodes(g)
    assert len(targets) >= 1
    if len(targets) == 1:
        return g
    ret = copy.deepcopy(g)

    def _next_available_idx(g):
        ret = -1
        for cn in g:
            if cn > ret:
                ret = cn
        ret += 1
        return ret

    target_node_idx = _next_available_idx(g)
    ret.add_node(target_node_idx)
    for cn in targets:
        ret.add_edge(cn, target_node_idx)

    return ret
