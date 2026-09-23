def test_invalid_auxiliary():
    G = nx.complete_graph(5)
    pytest.raises(nx.NetworkXError, minimum_st_node_cut, G, 0, 3, auxiliary=G)
