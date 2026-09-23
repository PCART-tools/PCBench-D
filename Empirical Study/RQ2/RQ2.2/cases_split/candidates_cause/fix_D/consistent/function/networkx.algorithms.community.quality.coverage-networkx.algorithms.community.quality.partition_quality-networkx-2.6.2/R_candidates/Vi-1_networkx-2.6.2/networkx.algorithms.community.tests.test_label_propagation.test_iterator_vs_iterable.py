def test_iterator_vs_iterable():
    G = nx.empty_graph("a")
    assert list(label_propagation_communities(G)) == [{"a"}]
    for community in label_propagation_communities(G):
        assert community == {"a"}
    pytest.raises(TypeError, next, label_propagation_communities(G))
