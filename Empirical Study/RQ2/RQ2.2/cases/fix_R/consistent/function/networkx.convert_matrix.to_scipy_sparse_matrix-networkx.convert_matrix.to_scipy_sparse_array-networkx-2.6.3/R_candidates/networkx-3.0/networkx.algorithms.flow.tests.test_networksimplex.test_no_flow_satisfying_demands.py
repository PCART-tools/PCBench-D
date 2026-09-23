def test_no_flow_satisfying_demands(simple_no_flow_graph):
    G = simple_no_flow_graph
    pytest.raises(nx.NetworkXUnfeasible, nx.network_simplex, G)
