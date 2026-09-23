def test_rechunk_with_zero_placeholders():
    x = da.ones((24, 24), chunks=((12, 12), (24, 0)))
    y = da.ones((24, 24), chunks=((12, 12), (12, 12)))
    y = y.rechunk(((12, 12), (24, 0)))
    assert x.chunks == y.chunks
