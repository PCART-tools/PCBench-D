def check_isomorphism(t1, t2, isomorphism):

    # get the name of t1, given the name in t2
    mapping = {v2: v1 for (v1, v2) in isomorphism}

    # these should be the same
    d1 = is_directed(t1)
    d2 = is_directed(t2)
    assert d1 == d2

    edges_1 = []
    for (u, v) in t1.edges():
        if d1:
            edges_1.append((u, v))
        else:
            # if not directed, then need to
            # put the edge in a consistent direction
            if u < v:
                edges_1.append((u, v))
            else:
                edges_1.append((v, u))

    edges_2 = []
    for (u, v) in t2.edges():
        # translate to names for t1
        u = mapping[u]
        v = mapping[v]
        if d2:
            edges_2.append((u, v))
        else:
            if u < v:
                edges_2.append((u, v))
            else:
                edges_2.append((v, u))

    return sorted(edges_1) == sorted(edges_2)
