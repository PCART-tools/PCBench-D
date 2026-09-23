def test_index_with_bool_dask_array_2():
    x = np.random.random((10, 10, 10))
    ind = np.random.random(10) > 0.5

    d = da.from_array(x, chunks=(3, 4, 5))
    dind = da.from_array(ind, chunks=4)

    index = [slice(1, 9, 1), slice(None)]

    for i in range(x.ndim):
        index2 = index[:]
        index2.insert(i, dind)

        index3 = index[:]
        index3.insert(i, ind)

        assert_eq(x[tuple(index3)], d[tuple(index2)])
