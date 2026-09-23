def test_empty_graphs():
    for k in range(5, 25, 5):
        G = nx.empty_graph(k)
        for flow_func in flow_funcs:
            errmsg = f"Assertion failed in function: {flow_func.__name__}"
            assert 0 == nx.node_connectivity(G, flow_func=flow_func), errmsg
            assert 0 == nx.edge_connectivity(G, flow_func=flow_func), errmsg
