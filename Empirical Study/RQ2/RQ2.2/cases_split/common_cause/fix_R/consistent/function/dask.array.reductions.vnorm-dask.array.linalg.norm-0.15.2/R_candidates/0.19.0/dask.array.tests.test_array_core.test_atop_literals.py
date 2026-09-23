def test_atop_literals():
    x = da.ones((10, 10), chunks=(5, 5))
    z = atop(add, 'ij', x, 'ij', 100, None, dtype=x.dtype)
    assert_eq(z, x + 100)

    z = atop(lambda x, y, z: x * y + z, 'ij', 2, None,  x, 'ij', 100, None, dtype=x.dtype)
    assert_eq(z, 2 * x + 100)

    z = atop(getitem, 'ij', x, 'ij', slice(None), None, dtype=x.dtype)
    assert_eq(z, x)
