def test_create_with_auto_dimensions():
    with dask.config.set({'array.chunk-size': '128MiB'}):
        x = da.random.random((10000, 10000), chunks=(-1, "auto"))
        assert x.chunks == ((10000,), (1250,) * 8)

        y = da.random.random((10000, 10000), chunks="auto")
        assert y.chunks == ((2500,) * 4, (2500,) * 4)
