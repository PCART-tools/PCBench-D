def test_arange():
    darr = da.arange(77, chunks=13)
    nparr = np.arange(77)
    assert_eq(darr, nparr)

    darr = da.arange(2, 13, chunks=5)
    nparr = np.arange(2, 13)
    assert_eq(darr, nparr)

    darr = da.arange(4, 21, 9, chunks=13)
    nparr = np.arange(4, 21, 9)
    assert_eq(darr, nparr)

    # negative steps
    darr = da.arange(53, 5, -3, chunks=5)
    nparr = np.arange(53, 5, -3)
    assert_eq(darr, nparr)

    darr = da.arange(77, chunks=13, dtype=float)
    nparr = np.arange(77, dtype=float)
    assert_eq(darr, nparr)

    darr = da.arange(2, 13, chunks=5, dtype=int)
    nparr = np.arange(2, 13, dtype=int)
    assert_eq(darr, nparr)
    assert sorted(da.arange(2, 13, chunks=5).dask) ==\
           sorted(da.arange(2, 13, chunks=5).dask)
    assert sorted(da.arange(77, chunks=13, dtype=float).dask) ==\
           sorted(da.arange(77, chunks=13, dtype=float).dask)
