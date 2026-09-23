def test_arange_has_dtype():
    assert da.arange(5, chunks=2)._dtype is not None
