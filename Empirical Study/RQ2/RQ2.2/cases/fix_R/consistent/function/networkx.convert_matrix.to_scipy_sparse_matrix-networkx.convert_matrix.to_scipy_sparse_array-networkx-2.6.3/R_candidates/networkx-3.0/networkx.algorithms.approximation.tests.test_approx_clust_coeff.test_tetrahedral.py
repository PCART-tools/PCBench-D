def test_tetrahedral():
    # Actual coefficient is 1
    G = nx.tetrahedral_graph()
    assert average_clustering(G, trials=len(G) // 2) == nx.average_clustering(G)
