def test_dodecahedral():
    # Actual coefficient is 0
    G = nx.dodecahedral_graph()
    assert average_clustering(G, trials=len(G) // 2) == nx.average_clustering(G)
