def test_atop_names():
    x = da.ones(5, chunks=(2,))
    y = atop(add, 'i', x, 'i', dtype=x.dtype)
    assert y.name.startswith('add')
