def test_from_array_chunks_dict():
    with dask.config.set({'array.chunk-size': '128kiB'}):
        x = np.empty((100, 100, 100))
        y = da.from_array(x, chunks={0: 10, 1: -1, 2: 'auto'})
        z = da.from_array(x, chunks=(10, 100, 10))
        assert y.chunks == z.chunks
