def test_slicing_consistent_names():
    x = np.arange(100).reshape((10, 10))
    a = da.from_array(x, chunks=(5, 5))
    assert same_keys(a[0], a[0])
    assert same_keys(a[:, [1, 2, 3]], a[:, [1, 2, 3]])
    assert same_keys(a[:, 5:2:-1], a[:, 5:2:-1])
