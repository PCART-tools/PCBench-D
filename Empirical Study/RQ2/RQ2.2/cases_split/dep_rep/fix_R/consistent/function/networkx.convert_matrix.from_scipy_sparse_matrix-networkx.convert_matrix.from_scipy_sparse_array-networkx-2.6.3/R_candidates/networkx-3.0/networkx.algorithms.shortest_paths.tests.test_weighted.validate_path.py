def validate_path(G, s, t, soln_len, path, weight="weight"):
    assert path[0] == s
    assert path[-1] == t

    if callable(weight):
        weight_f = weight
    else:
        if G.is_multigraph():

            def weight_f(u, v, d):
                return min(e.get(weight, 1) for e in d.values())

        else:

            def weight_f(u, v, d):
                return d.get(weight, 1)

    computed = sum(weight_f(u, v, G[u][v]) for u, v in pairwise(path))
    assert soln_len == computed
