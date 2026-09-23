def test_articulation_points():
    Ggen = _generate_no_biconnected()
    for flow_func in flow_funcs:
        for i in range(3):
            G = next(Ggen)
            errmsg = f"Assertion failed in function: {flow_func.__name__}"
            assert nx.node_connectivity(G, flow_func=flow_func) == 1, errmsg
