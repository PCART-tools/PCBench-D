def test_keys():
    dsk = dict((('x', i, j), ()) for i in range(5) for j in range(6))
    dx = Array(dsk, 'x', chunks=(10, 10), shape=(50, 60), dtype='f8')
    assert dx.__dask_keys__() == [[(dx.name, i, j) for j in range(6)]
                                  for i in range(5)]
    # Cache works
    assert dx.__dask_keys__() is dx.__dask_keys__()
    # Test mutating names clears key cache
    dx.dask = {('y', i, j): () for i in range(5) for j in range(6)}
    dx.name = 'y'
    assert dx.__dask_keys__() == [[(dx.name, i, j) for j in range(6)]
                                  for i in range(5)]
    d = Array({}, 'x', (), shape=(), dtype='f8')
    assert d.__dask_keys__() == [('x',)]
