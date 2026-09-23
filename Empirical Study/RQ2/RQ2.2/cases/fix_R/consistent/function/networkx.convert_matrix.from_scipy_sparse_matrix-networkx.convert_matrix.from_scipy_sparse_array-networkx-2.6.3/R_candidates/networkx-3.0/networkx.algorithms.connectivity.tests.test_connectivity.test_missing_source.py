def test_missing_source():
    G = nx.path_graph(4)
    for flow_func in flow_funcs:
        pytest.raises(
            nx.NetworkXError, nx.node_connectivity, G, 10, 1, flow_func=flow_func
        )
