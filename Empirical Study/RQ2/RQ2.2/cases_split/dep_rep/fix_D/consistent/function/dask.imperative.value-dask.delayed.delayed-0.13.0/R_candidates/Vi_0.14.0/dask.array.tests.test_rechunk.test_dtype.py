def test_dtype():
    x = da.ones(5, chunks=(2,))
    assert x.rechunk(chunks=(1,)).dtype == x.dtype
