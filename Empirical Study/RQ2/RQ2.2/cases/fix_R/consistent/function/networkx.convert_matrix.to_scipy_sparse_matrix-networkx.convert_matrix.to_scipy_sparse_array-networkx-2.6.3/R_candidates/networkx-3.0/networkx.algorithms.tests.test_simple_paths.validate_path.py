def validate_path(G, s, t, soln_len, path):
    assert path[0] == s
    assert path[-1] == t
    assert soln_len == sum(
        G[u][v].get("weight", 1) for u, v in zip(path[:-1], path[1:])
    )
