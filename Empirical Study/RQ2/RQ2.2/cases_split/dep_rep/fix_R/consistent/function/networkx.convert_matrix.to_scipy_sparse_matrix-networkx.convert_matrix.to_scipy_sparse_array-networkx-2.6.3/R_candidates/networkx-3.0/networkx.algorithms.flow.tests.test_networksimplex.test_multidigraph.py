def test_multidigraph():
    """Multidigraphs are acceptable."""
    G = nx.MultiDiGraph()
    G.add_weighted_edges_from([(1, 2, 1), (2, 3, 2)], weight="capacity")
    flowCost, H = nx.network_simplex(G)
    assert flowCost == 0
    assert H == {1: {2: {0: 0}}, 2: {3: {0: 0}}, 3: {}}
