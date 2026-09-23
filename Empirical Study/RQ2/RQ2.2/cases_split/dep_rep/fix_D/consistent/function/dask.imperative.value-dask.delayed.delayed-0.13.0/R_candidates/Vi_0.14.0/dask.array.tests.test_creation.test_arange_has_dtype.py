def test_arange_has_dtype():
    assert da.arange(5, chunks=2).dtype == np.arange(5).dtype
