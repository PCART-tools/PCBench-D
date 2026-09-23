@pytest.mark.skipif(no_backends_for_leiden_communities)
def test_none_weight_param():
    G = nx.karate_club_graph()
    nx.set_edge_attributes(
        G, {edge: i * i for i, edge in enumerate(G.edges)}, name="foo"
    )

    partition1 = nx.community.leiden_communities(G, weight=None, seed=2)
    partition2 = nx.community.leiden_communities(G, weight="foo", seed=2)
    partition3 = nx.community.leiden_communities(G, weight="weight", seed=2)

    assert partition1 != partition2
    assert partition2 != partition3
