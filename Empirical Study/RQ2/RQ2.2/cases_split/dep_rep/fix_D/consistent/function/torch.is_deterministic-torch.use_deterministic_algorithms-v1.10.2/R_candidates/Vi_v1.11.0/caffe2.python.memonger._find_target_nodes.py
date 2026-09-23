def _find_target_nodes(g):
    ''' Return nodes without successors '''
    ret = []
    for cn in g:
        cur_succ = list(g.successors(cn))
        if not cur_succ:
            ret.append(cn)
    return ret
