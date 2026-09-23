def test_octahedral():
    G = nx.octahedral_graph()
    assert 4 == approx.node_connectivity(G)
    assert 4 == approx.node_connectivity(G, 0, 5)
