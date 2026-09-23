def _min_cycle_basis(comp, weight):
    cb = []
    # We  extract the edges not in a spanning tree. We do not really need a
    # *minimum* spanning tree. That is why we call the next function with
    # weight=None. Depending on implementation, it may be faster as well
    spanning_tree_edges = list(nx.minimum_spanning_edges(comp, weight=None, data=False))
    edges_excl = [frozenset(e) for e in comp.edges() if e not in spanning_tree_edges]
    N = len(edges_excl)

    # We maintain a set of vectors orthogonal to sofar found cycles
    set_orth = [{edge} for edge in edges_excl]
    for k in range(N):
        # kth cycle is "parallel" to kth vector in set_orth
        new_cycle = _min_cycle(comp, set_orth[k], weight=weight)
        cb.append(list(set().union(*new_cycle)))
        # now update set_orth so that k+1,k+2... th elements are
        # orthogonal to the newly found cycle, as per [p. 336, 1]
        base = set_orth[k]
        set_orth[k + 1 :] = [
            orth ^ base if len(orth & new_cycle) % 2 else orth
            for orth in set_orth[k + 1 :]
        ]
    return cb
