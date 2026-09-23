def test_basic():
    # sanity check
    dtype = [('a', 'f8'), ('b', 'f8'), ('c', 'f8')]
    x = np.ones((5, 3), dtype=dtype)
    dx = da.ones((5, 3), dtype=dtype, chunks=3)
    result = dx[['a', 'b']]
    expected = x[['a', 'b']]
    assert_eq(result, expected)
