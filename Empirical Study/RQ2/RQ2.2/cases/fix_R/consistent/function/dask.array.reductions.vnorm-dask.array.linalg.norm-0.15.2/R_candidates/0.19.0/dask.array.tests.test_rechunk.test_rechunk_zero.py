def test_rechunk_zero():
    with dask.config.set({'array.chunk-size': '1B'}):
        x = da.ones(10, chunks=(5,))
        y = x.rechunk('auto')
        assert y.chunks == ((1,) * 10,)
