def test_empty_graphs():
    for k in range(5, 25, 5):
        G = nx.empty_graph(k)
        assert 0 == approx.node_connectivity(G)
        assert 0 == approx.node_connectivity(G, 0, 3)
