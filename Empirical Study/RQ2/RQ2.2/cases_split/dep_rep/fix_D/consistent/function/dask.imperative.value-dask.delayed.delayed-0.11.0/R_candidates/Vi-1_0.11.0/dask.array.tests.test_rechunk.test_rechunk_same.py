def test_rechunk_same():
    x = da.ones((24, 24), chunks=(4, 8))
    y = x.rechunk(x.chunks)
    assert x is y
