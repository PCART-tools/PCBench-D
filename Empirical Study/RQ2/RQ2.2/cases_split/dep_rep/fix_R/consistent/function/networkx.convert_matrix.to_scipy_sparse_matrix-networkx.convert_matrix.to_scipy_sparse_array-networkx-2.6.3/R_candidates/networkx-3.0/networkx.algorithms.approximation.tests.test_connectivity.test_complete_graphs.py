def test_complete_graphs():
    for n in range(5, 25, 5):
        G = nx.complete_graph(n)
        assert n - 1 == approx.node_connectivity(G)
        assert n - 1 == approx.node_connectivity(G, 0, 3)
