def test_petersen():
    G = nx.petersen_graph()
    assert 3 == approx.node_connectivity(G)
    assert 3 == approx.node_connectivity(G, 0, 5)
