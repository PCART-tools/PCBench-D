def test_complete():
    G = nx.complete_graph(5)
    assert average_clustering(G, trials=len(G) // 2) == 1
    G = nx.complete_graph(7)
    assert average_clustering(G, trials=len(G) // 2) == 1
