def test_shell():
    # seeds = [2057382236, 3331169846, 1840105863, 476020778, 2247498425]
    seeds = [20]
    for seed in seeds:
        constructor = [(12, 70, 0.8), (15, 40, 0.6)]
        G = nx.random_shell_graph(constructor, seed=seed)
        _check_edge_connectivity(G)
