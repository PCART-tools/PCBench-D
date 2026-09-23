def test_not_weakly_connected():
    G = nx.DiGraph()
    nx.add_path(G, [1, 2, 3])
    nx.add_path(G, [4, 5])
    for interface_func in [nx.minimum_edge_cut, nx.minimum_node_cut]:
        for flow_func in flow_funcs:
            pytest.raises(nx.NetworkXError, interface_func, G, flow_func=flow_func)
