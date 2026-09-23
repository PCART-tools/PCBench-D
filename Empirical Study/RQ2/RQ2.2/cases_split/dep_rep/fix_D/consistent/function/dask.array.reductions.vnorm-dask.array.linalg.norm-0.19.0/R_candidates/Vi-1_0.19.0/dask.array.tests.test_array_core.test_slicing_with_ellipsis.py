def test_slicing_with_ellipsis():
    x = np.arange(256).reshape((4, 4, 4, 4))
    d = da.from_array(x, chunks=((2, 2, 2, 2)))

    assert_eq(d[..., 1], x[..., 1])
    assert_eq(d[0, ..., 1], x[0, ..., 1])
