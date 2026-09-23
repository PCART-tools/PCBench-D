def test_unknown_algorithm():
    with pytest.raises(ValueError):
        nx.minimum_spanning_tree(nx.Graph(), algorithm="random")
