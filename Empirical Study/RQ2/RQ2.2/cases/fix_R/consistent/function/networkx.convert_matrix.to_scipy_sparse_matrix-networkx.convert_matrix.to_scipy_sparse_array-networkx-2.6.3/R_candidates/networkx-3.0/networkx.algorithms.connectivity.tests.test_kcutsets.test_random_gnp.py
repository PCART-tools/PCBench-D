def test_random_gnp():
    G = nx.gnp_random_graph(100, 0.1, seed=42)
    _check_separating_sets(G)
