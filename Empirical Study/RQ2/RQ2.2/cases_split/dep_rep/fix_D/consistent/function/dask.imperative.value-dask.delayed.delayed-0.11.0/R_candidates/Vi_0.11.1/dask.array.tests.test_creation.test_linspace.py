def test_linspace():
    darr = da.linspace(6, 49, chunks=5)
    nparr = np.linspace(6, 49)
    assert_eq(darr, nparr)

    darr = da.linspace(1.4, 4.9, chunks=5, num=13)
    nparr = np.linspace(1.4, 4.9, num=13)
    assert_eq(darr, nparr)

    darr = da.linspace(6, 49, chunks=5, dtype=float)
    nparr = np.linspace(6, 49, dtype=float)
    assert_eq(darr, nparr)

    darr = da.linspace(1.4, 4.9, chunks=5, num=13, dtype=int)
    nparr = np.linspace(1.4, 4.9, num=13, dtype=int)
    assert_eq(darr, nparr)
    assert sorted(da.linspace(1.4, 4.9, chunks=5, num=13).dask) ==\
           sorted(da.linspace(1.4, 4.9, chunks=5, num=13).dask)
    assert sorted(da.linspace(6, 49, chunks=5, dtype=float).dask) ==\
           sorted(da.linspace(6, 49, chunks=5, dtype=float).dask)
