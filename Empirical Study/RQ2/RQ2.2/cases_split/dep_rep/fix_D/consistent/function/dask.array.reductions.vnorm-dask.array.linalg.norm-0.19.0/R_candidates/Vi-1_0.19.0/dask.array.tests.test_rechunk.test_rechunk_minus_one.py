def test_rechunk_minus_one():
    x = da.ones((24, 24), chunks=(4, 8))
    y = x.rechunk((-1, 8))
    assert y.chunks == ((24,), (8, 8, 8))
    assert_eq(x, y)
