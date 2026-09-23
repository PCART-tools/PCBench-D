def test_missing_source():
    G = nx.path_graph(4)
    pytest.raises(nx.NetworkXError, approx.node_connectivity, G, 10, 1)
