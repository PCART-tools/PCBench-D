def test_empty():
    G = nx.empty_graph(5)
    assert average_clustering(G, trials=len(G) // 2) == 0
