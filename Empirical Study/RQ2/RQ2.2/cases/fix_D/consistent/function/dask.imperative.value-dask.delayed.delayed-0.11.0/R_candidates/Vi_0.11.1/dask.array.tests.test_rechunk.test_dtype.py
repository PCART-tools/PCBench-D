def test_dtype():
    x = da.ones(5, chunks=(2,))
    assert x.rechunk(chunks=(1,))._dtype == x._dtype
