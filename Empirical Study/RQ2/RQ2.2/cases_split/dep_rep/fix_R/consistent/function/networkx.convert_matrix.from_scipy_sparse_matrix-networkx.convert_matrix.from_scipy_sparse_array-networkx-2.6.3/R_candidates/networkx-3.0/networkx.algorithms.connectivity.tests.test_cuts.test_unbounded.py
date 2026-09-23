def test_unbounded():
    G = nx.complete_graph(5)
    for flow_func in flow_funcs:
        assert 4 == len(minimum_st_edge_cut(G, 1, 4, flow_func=flow_func))
