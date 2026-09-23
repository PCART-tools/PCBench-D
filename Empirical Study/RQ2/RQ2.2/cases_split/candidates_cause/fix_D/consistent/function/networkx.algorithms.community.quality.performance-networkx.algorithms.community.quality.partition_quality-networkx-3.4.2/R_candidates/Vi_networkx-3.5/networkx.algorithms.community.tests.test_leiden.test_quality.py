@pytest.mark.skipif(no_backends_for_leiden_communities)
def test_quality():
    G = nx.LFR_benchmark_graph(
        250, 3, 1.5, 0.009, average_degree=5, min_community=20, seed=10
    )
    H = nx.MultiGraph(G)

    partition = nx.community.leiden_communities(G)
    partition2 = nx.community.leiden_communities(H)

    quality = nx.community.partition_quality(G, partition)[0]
    quality2 = nx.community.partition_quality(H, partition2)[0]

    assert quality >= 0.65
    assert quality2 >= 0.65
