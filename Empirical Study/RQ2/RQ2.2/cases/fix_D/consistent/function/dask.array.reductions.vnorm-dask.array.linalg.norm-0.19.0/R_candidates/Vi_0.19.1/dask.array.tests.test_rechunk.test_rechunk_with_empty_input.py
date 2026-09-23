def test_rechunk_with_empty_input():
    x = da.ones((24, 24), chunks=(4, 8))
    assert x.rechunk(chunks={}).chunks == x.chunks
    pytest.raises(ValueError, lambda: x.rechunk(chunks=()))
