def test_stack():
    a, b, c = [Array(getem(name, chunks=(2, 3), shape=(4, 6)),
                     name, chunks=(2, 3), dtype='f8', shape=(4, 6))
               for name in 'ABC']

    s = stack([a, b, c], axis=0)

    colon = slice(None, None, None)

    assert s.shape == (3, 4, 6)
    assert s.chunks == ((1, 1, 1), (2, 2), (3, 3))
    assert s.chunksize == (1, 2, 3)
    assert s.dask[(s.name, 0, 1, 0)] == (getitem, ('A', 1, 0),
                                         (None, colon, colon))
    assert s.dask[(s.name, 2, 1, 0)] == (getitem, ('C', 1, 0),
                                         (None, colon, colon))
    assert same_keys(s, stack([a, b, c], axis=0))

    s2 = stack([a, b, c], axis=1)
    assert s2.shape == (4, 3, 6)
    assert s2.chunks == ((2, 2), (1, 1, 1), (3, 3))
    assert s2.chunksize == (2, 1, 3)
    assert s2.dask[(s2.name, 0, 1, 0)] == (getitem, ('B', 0, 0),
                                           (colon, None, colon))
    assert s2.dask[(s2.name, 1, 1, 0)] == (getitem, ('B', 1, 0),
                                           (colon, None, colon))
    assert same_keys(s2, stack([a, b, c], axis=1))

    s2 = stack([a, b, c], axis=2)
    assert s2.shape == (4, 6, 3)
    assert s2.chunks == ((2, 2), (3, 3), (1, 1, 1))
    assert s2.chunksize == (2, 3, 1)
    assert s2.dask[(s2.name, 0, 1, 0)] == (getitem, ('A', 0, 1),
                                           (colon, colon, None))
    assert s2.dask[(s2.name, 1, 1, 2)] == (getitem, ('C', 1, 1),
                                           (colon, colon, None))
    assert same_keys(s2, stack([a, b, c], axis=2))

    pytest.raises(ValueError, lambda: stack([a, b, c], axis=3))

    assert set(b.dask.keys()).issubset(s2.dask.keys())

    assert stack([a, b, c], axis=-1).chunks == stack([a, b, c], axis=2).chunks
