def test_slicing_consistent_names_after_normalization():
    x = da.zeros(10, chunks=(5,))
    assert same_keys(x[0:], x[:10])
    assert same_keys(x[0:], x[0:10])
    assert same_keys(x[0:], x[0:10:1])
    assert same_keys(x[:], x[0:10:1])
