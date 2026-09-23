def test_not_covering():
    G = nx.empty_graph(3)
    assert not is_partition(G, [{0}, {1}])
