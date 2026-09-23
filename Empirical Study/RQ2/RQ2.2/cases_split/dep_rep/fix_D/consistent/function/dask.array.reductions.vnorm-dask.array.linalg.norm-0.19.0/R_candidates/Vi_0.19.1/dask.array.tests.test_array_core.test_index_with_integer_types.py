def test_index_with_integer_types():
    x = np.arange(10)
    dx = da.from_array(x, chunks=5)
    inds = int(3)
    assert_eq(dx[inds], x[inds])

    inds = np.int64(3)
    assert_eq(dx[inds], x[inds])
