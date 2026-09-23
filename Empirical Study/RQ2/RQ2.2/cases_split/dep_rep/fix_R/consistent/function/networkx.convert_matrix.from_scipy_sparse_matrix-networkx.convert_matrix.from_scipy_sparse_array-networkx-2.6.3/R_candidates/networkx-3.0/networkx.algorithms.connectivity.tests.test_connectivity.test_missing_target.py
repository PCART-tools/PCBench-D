def test_missing_target():
    G = nx.path_graph(4)
    for flow_func in flow_funcs:
        pytest.raises(
            nx.NetworkXError, nx.node_connectivity, G, 1, 10, flow_func=flow_func
        )
