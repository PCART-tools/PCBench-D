def test_interface_only_target():
    G = nx.complete_graph(5)
    for interface_func in [nx.minimum_node_cut, nx.minimum_edge_cut]:
        pytest.raises(nx.NetworkXError, interface_func, G, t=3)
