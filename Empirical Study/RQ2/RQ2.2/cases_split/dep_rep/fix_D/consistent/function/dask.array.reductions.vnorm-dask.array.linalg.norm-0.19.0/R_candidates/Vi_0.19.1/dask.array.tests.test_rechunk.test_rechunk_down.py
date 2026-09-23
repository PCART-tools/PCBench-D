def test_rechunk_down():
    with dask.config.set({'array.chunk-size': '10MiB'}):
        x = da.ones((100, 1000, 1000), chunks=(1, 1000, 1000), dtype='uint8')
        y = x.rechunk('auto')
        assert y.chunks == ((10,) * 10, (1000,), (1000,))

    with dask.config.set({'array.chunk-size': '1MiB'}):
        z = y.rechunk('auto')
        assert z.chunks == ((5,) * 20, (250,) * 4, (250,) * 4)

    with dask.config.set({'array.chunk-size': '1MiB'}):
        z = y.rechunk({0: 'auto'})
        assert z.chunks == ((1,) * 100, (1000,),  (1000,))

        z = y.rechunk({1: 'auto'})
        assert z.chunks == ((10,) * 10, (100,) * 10,  (1000,))
