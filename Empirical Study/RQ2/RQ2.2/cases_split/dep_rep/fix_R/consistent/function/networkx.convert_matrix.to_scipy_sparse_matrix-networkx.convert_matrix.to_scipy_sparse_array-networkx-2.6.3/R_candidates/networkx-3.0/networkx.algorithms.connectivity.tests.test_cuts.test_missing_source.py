def test_missing_source():
    G = nx.path_graph(4)
    for interface_func in [nx.minimum_edge_cut, nx.minimum_node_cut]:
        for flow_func in flow_funcs:
            pytest.raises(
                nx.NetworkXError, interface_func, G, 10, 1, flow_func=flow_func
            )
