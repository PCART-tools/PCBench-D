def test_diag():
    v = np.arange(11)
    assert_eq(da.diag(v), np.diag(v))

    v = da.arange(11, chunks=3)
    darr = da.diag(v)
    nparr = np.diag(v)
    assert_eq(darr, nparr)
    assert sorted(da.diag(v).dask) == sorted(da.diag(v).dask)

    v = v + v + 3
    darr = da.diag(v)
    nparr = np.diag(v)
    assert_eq(darr, nparr)

    v = da.arange(11, chunks=11)
    darr = da.diag(v)
    nparr = np.diag(v)
    assert_eq(darr, nparr)
    assert sorted(da.diag(v).dask) == sorted(da.diag(v).dask)

    x = np.arange(64).reshape((8, 8))
    assert_eq(da.diag(x), np.diag(x))

    d = da.from_array(x, chunks=(4, 4))
    assert_eq(da.diag(d), np.diag(x))
