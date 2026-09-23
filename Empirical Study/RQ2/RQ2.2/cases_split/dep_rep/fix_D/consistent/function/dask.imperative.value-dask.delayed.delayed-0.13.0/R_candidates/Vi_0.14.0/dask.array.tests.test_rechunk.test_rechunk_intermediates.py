def test_rechunk_intermediates():
    x = da.random.normal(10, 0.1, (10, 10), chunks=(10, 1))
    y = x.rechunk((1, 10))
    assert len(y.dask) > 30
