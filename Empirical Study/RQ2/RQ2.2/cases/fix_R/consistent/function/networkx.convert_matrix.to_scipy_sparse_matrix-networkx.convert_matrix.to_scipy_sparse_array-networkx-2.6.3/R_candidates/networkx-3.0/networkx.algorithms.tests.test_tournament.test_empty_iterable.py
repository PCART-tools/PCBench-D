def test_empty_iterable():
    condition = lambda x: x > 0
    with pytest.raises(ValueError):
        index_satisfying([], condition)
