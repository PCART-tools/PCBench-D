def test_rechunk_empty():
    x = da.ones((0, 10), chunks=(5, 5))
    y = x.rechunk((2, 2))
    assert y.chunks == ((0,), (2,) * 5)
    assert_eq(x, y)
