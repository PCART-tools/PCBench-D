def test_complete_graph():
    G = nx.complete_graph(5)
    solution = [{0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 3, 4}, {0, 2, 3, 4}, {1, 2, 3, 4}]
    cuts = list(nx.all_node_cuts(G))
    assert len(solution) == len(cuts)
    for cut in cuts:
        assert cut in solution
