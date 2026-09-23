def test_Array():
    shape = (1000, 1000)
    chunks = (100, 100)
    name = 'x'
    dsk = merge({name: 'some-array'}, getem(name, chunks, shape=shape))
    a = Array(dsk, name, chunks, shape=shape, dtype='f8')

    assert a.numblocks == (10, 10)

    assert a.__dask_keys__() == [[('x', i, j) for j in range(10)]
                                 for i in range(10)]

    assert a.chunks == ((100,) * 10, (100,) * 10)

    assert a.shape == shape

    assert len(a) == shape[0]
