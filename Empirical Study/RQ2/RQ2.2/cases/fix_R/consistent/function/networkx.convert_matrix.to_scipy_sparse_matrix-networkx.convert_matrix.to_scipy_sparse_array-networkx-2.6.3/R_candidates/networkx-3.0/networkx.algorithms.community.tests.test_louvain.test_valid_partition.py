def test_valid_partition():
    G = nx.LFR_benchmark_graph(
        250, 3, 1.5, 0.009, average_degree=5, min_community=20, seed=10
    )
    H = G.to_directed()
    partition = louvain_communities(G)
    partition2 = louvain_communities(H)

    assert is_partition(G, partition)
    assert is_partition(H, partition2)
