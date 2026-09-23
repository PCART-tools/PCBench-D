def test_concatenate():
    a, b, c = [Array(getem(name, chunks=(2, 3), shape=(4, 6)),
                     name, chunks=(2, 3), dtype='f8', shape=(4, 6))
               for name in 'ABC']

    x = concatenate([a, b, c], axis=0)

    assert x.shape == (12, 6)
    assert x.chunks == ((2, 2, 2, 2, 2, 2), (3, 3))
    assert x.dask[(x.name, 0, 1)] == ('A', 0, 1)
    assert x.dask[(x.name, 5, 0)] == ('C', 1, 0)
    assert same_keys(x, concatenate([a, b, c], axis=0))

    y = concatenate([a, b, c], axis=1)

    assert y.shape == (4, 18)
    assert y.chunks == ((2, 2), (3, 3, 3, 3, 3, 3))
    assert y.dask[(y.name, 1, 0)] == ('A', 1, 0)
    assert y.dask[(y.name, 1, 5)] == ('C', 1, 1)
    assert same_keys(y, concatenate([a, b, c], axis=1))

    assert set(b.dask.keys()).issubset(y.dask.keys())

    z = concatenate([a], axis=0)

    assert z.shape == a.shape
    assert z.chunks == a.chunks
    assert z.dask == a.dask
    assert z is a

    assert (concatenate([a, b, c], axis=-1).chunks ==
            concatenate([a, b, c], axis=1).chunks)

    pytest.raises(ValueError, lambda: concatenate([a, b, c], axis=2))
