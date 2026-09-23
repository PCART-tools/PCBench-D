def test_numblocks_suppoorts_singleton_block_dims():
    shape = (100, 10)
    chunks = (10, 10)
    name = 'x'
    dsk = merge({name: 'some-array'}, getem(name, shape=shape, chunks=chunks))
    a = Array(dsk, name, chunks, shape=shape, dtype='f8')

    assert set(concat(a.__dask_keys__())) == {('x', i, 0) for i in range(10)}
