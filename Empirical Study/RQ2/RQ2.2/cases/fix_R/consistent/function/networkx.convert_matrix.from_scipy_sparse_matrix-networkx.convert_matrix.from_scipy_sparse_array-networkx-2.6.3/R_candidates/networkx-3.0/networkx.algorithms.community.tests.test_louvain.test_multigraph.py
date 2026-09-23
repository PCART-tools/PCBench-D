def test_multigraph():
    G = nx.karate_club_graph()
    H = nx.MultiGraph(G)
    G.add_edge(0, 1, weight=10)
    H.add_edge(0, 1, weight=9)
    G.add_edge(0, 9, foo=20)
    H.add_edge(0, 9, foo=20)

    partition1 = louvain_communities(G, seed=1234)
    partition2 = louvain_communities(H, seed=1234)
    partition3 = louvain_communities(H, weight="foo", seed=1234)

    assert partition1 == partition2 != partition3
