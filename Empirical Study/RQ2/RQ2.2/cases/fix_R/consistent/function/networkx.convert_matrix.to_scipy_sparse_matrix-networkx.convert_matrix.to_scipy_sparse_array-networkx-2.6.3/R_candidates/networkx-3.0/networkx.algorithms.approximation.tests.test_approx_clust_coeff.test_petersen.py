def test_petersen():
    # Actual coefficient is 0
    G = nx.petersen_graph()
    assert average_clustering(G, trials=len(G) // 2) == nx.average_clustering(G)
