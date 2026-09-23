def test_not_disjoint():
    G = nx.empty_graph(3)
    assert not is_partition(G, [{0, 1}, {1, 2}])
