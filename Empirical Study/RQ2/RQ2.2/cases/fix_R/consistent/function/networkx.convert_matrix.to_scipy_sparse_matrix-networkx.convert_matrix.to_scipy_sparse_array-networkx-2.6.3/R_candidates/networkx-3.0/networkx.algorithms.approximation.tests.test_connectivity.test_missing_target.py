def test_missing_target():
    G = nx.path_graph(4)
    pytest.raises(nx.NetworkXError, approx.node_connectivity, G, 1, 10)
