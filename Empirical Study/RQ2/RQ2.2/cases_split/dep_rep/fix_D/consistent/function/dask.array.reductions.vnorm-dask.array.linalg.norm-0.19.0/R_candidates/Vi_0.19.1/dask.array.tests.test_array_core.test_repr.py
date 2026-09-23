def test_repr():
    d = da.ones((4, 4), chunks=(2, 2))
    assert key_split(d.name) in repr(d)
    assert str(d.shape) in repr(d)
    assert str(d.dtype) in repr(d)
    d = da.ones((4000, 4), chunks=(4, 2))
    assert len(str(d)) < 1000
