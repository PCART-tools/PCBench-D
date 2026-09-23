def validate_path(G, s, t, soln_len, path):
    assert_equal(path[0], s)
    assert_equal(path[-1], t)
    if not G.is_multigraph():
        computed = sum(G[u][v].get('weight', 1) for u, v in pairwise(path))
        assert_equal(soln_len, computed)
    else:
        computed = sum(min(e.get('weight', 1) for e in G[u][v].values())
                       for u, v in pairwise(path))
        assert_equal(soln_len, computed)
