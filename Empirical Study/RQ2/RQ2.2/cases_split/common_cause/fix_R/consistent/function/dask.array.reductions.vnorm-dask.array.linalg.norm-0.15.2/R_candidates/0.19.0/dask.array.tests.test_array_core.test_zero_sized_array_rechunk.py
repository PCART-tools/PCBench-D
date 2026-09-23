def test_zero_sized_array_rechunk():
    x = da.arange(5, chunks=1)[:0]
    y = da.atop(identity, 'i', x, 'i', dtype=x.dtype)
    assert_eq(x, y)
