def test_empty_graphs():
    G = nx.Graph()
    D = nx.DiGraph()
    for interface_func in [nx.minimum_node_cut, nx.minimum_edge_cut]:
        for flow_func in flow_funcs:
            pytest.raises(
                nx.NetworkXPointlessConcept, interface_func, G, flow_func=flow_func
            )
            pytest.raises(
                nx.NetworkXPointlessConcept, interface_func, D, flow_func=flow_func
            )
