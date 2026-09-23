def test_graph_iterable():
    K = nx.complete_graph(10)
    assert iterable(K)
    assert iterable(K.nodes())
    assert iterable(K.edges())
