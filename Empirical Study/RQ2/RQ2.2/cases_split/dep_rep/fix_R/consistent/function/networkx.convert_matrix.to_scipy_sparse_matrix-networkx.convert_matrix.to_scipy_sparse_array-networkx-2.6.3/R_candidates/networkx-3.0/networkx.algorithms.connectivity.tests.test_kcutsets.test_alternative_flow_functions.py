@pytest.mark.slow
def test_alternative_flow_functions():
    graphs = [nx.grid_2d_graph(4, 4), nx.cycle_graph(5)]
    for G in graphs:
        node_conn = nx.node_connectivity(G)
        for flow_func in flow_funcs:
            all_cuts = nx.all_node_cuts(G, flow_func=flow_func)
            # Only test a limited number of cut sets to reduce test time.
            for cut in itertools.islice(all_cuts, MAX_CUTSETS_TO_TEST):
                assert node_conn == len(cut)
                assert not nx.is_connected(nx.restricted_view(G, cut, []))
