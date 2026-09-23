def _find_source_nodes(g):
    ''' Return nodes without predecessors '''
    ret = []
    for cn in g:
        cur_pred = list(g.predecessors(cn))
        if not cur_pred:
            ret.append(cn)
    return ret
