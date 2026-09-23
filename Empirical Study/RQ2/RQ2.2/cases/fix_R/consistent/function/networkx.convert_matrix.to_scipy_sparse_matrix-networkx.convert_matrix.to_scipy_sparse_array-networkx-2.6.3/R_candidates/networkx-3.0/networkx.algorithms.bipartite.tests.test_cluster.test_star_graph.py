def test_star_graph():
    G = nx.star_graph(3)
    # all modes are the same
    answer = {0: 0, 1: 1, 2: 1, 3: 1}
    assert bipartite.clustering(G, mode="dot") == answer
    assert bipartite.clustering(G, mode="min") == answer
    assert bipartite.clustering(G, mode="max") == answer
