def test_binops():
    a = Array(dict((('a', i), np.array([0])) for i in range(3)),
              'a', chunks=((1, 1, 1),), dtype='i8')
    b = Array(dict((('b', i), np.array([0])) for i in range(3)),
              'b', chunks=((1, 1, 1),), dtype='i8')

    result = elemwise(add, a, b, name='c')
    assert result.dask == merge(a.dask, b.dask,
                                dict((('c', i), (add, ('a', i), ('b', i)))
                                     for i in range(3)))

    result = elemwise(pow, a, 2, name='c')
    assert "'a', 0" in str(result.dask[('c', 0)])
    assert "2" in str(result.dask[('c', 0)])
