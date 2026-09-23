def test_weight_name():
    G = nx.Graph()
    G.add_edge(1, 2, weight=1, cost=8)
    G.add_edge(1, 3, cost=2)
    G.add_edge(2, 3, cost=4)
    _test_stoer_wagner(G, 6, weight="cost")
