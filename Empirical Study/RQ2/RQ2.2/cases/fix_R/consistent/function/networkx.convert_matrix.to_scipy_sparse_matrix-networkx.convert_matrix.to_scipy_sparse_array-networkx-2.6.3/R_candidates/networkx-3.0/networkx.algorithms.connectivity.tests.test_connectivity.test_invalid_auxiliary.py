def test_invalid_auxiliary():
    G = nx.complete_graph(5)
    pytest.raises(nx.NetworkXError, local_node_connectivity, G, 0, 3, auxiliary=G)
