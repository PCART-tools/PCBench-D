@pytest.mark.skipif(no_backends_for_leiden_communities)
def test_valid_partition():
    G = nx.LFR_benchmark_graph(
        250, 3, 1.5, 0.009, average_degree=5, min_community=20, seed=10
    )
    partition = nx.community.leiden_communities(G)

    assert nx.community.is_partition(G, partition)
