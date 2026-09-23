def test_from_array_with_missing_chunks():
    x = np.random.randn(2, 4, 3)
    d = da.from_array(x, chunks=(None, 2, None))
    assert d.chunks == da.from_array(x, chunks=(2, 2, 3)).chunks
