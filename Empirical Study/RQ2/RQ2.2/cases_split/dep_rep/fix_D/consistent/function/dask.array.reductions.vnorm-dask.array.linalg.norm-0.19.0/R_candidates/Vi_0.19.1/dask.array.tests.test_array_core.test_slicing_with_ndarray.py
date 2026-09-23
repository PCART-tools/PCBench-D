def test_slicing_with_ndarray():
    x = np.arange(64).reshape((8, 8))
    d = da.from_array(x, chunks=((4, 4)))

    assert_eq(d[np.arange(8)], x)
    assert_eq(d[np.ones(8, dtype=bool)], x)
    assert_eq(d[np.array([1])], x[[1]])
    assert_eq(d[np.array([True, False, True] + [False] * 5)], x[[0, 2]])
