@pytest.mark.parametrize('n', [100, 1000])
def test_rechunk_auto_image_stack(n):
    with dask.config.set({'array.chunk-size': '10MiB'}):
        x = da.ones((n, 1000, 1000), chunks=(1, 1000, 1000), dtype='uint8')
        y = x.rechunk('auto')
        assert y.chunks == ((10,) * (n // 10), (1000,), (1000,))
        assert y.rechunk('auto').chunks == y.chunks  # idempotent

    with dask.config.set({'array.chunk-size': '7MiB'}):
        z = x.rechunk('auto')
        assert z.chunks == ((5,) * (n // 5), (1000,), (1000,))

    with dask.config.set({'array.chunk-size': '1MiB'}):
        x = da.ones((n, 1000, 1000), chunks=(1, 1000, 1000), dtype='float64')
        z = x.rechunk('auto')
        assert z.chunks == ((1,) * n , (250,) * 4, (250,) * 4)
