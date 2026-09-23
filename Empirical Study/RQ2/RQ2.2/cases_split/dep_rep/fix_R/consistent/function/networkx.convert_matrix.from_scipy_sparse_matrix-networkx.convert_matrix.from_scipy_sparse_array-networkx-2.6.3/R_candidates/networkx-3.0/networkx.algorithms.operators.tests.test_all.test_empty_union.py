def test_empty_union():
    with pytest.raises(ValueError):
        nx.union_all([])
