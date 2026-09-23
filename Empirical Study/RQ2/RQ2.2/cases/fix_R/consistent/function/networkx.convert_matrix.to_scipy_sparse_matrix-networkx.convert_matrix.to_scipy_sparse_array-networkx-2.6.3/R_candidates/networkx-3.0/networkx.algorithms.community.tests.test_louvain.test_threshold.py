def test_threshold():
    G = nx.LFR_benchmark_graph(
        250, 3, 1.5, 0.009, average_degree=5, min_community=20, seed=10
    )
    partition1 = louvain_communities(G, threshold=0.3, seed=2)
    partition2 = louvain_communities(G, seed=2)
    mod1 = modularity(G, partition1)
    mod2 = modularity(G, partition2)

    assert mod1 < mod2
