@pytest.mark.parametrize("endpoint", [True, False])
def test_linspace(endpoint):
    darr = da.linspace(6, 49, endpoint=endpoint, chunks=5)
    nparr = np.linspace(6, 49, endpoint=endpoint)
    assert_eq(darr, nparr)

    darr = da.linspace(1.4, 4.9, endpoint=endpoint, chunks=5, num=13)
    nparr = np.linspace(1.4, 4.9, endpoint=endpoint, num=13)
    assert_eq(darr, nparr)

    darr = da.linspace(6, 49, endpoint=endpoint, chunks=5, dtype=float)
    nparr = np.linspace(6, 49, endpoint=endpoint, dtype=float)
    assert_eq(darr, nparr)

    darr, dstep = da.linspace(6, 49, endpoint=endpoint, chunks=5, retstep=True)
    nparr, npstep = np.linspace(6, 49, endpoint=endpoint, retstep=True)
    assert np.allclose(dstep, npstep)
    assert_eq(darr, nparr)

    darr = da.linspace(1.4, 4.9, endpoint=endpoint, chunks=5, num=13, dtype=int)
    nparr = np.linspace(1.4, 4.9, num=13, endpoint=endpoint, dtype=int)
    assert_eq(darr, nparr)
    assert (sorted(da.linspace(1.4, 4.9, endpoint=endpoint, chunks=5, num=13).dask) ==
            sorted(da.linspace(1.4, 4.9, endpoint=endpoint, chunks=5, num=13).dask))
    assert (sorted(da.linspace(6, 49, endpoint=endpoint, chunks=5, dtype=float).dask) ==
            sorted(da.linspace(6, 49, endpoint=endpoint, chunks=5, dtype=float).dask))
