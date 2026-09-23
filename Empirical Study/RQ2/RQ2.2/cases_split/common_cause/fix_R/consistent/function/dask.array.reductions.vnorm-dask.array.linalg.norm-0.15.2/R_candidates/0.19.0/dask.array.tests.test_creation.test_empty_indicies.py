def test_empty_indicies():
    darr = da.indices(tuple(), chunks=tuple())
    nparr = np.indices(tuple())
    assert darr.shape == nparr.shape
    assert darr.dtype == nparr.dtype
    assert_eq(darr, nparr)

    darr = da.indices(tuple(), float, chunks=tuple())
    nparr = np.indices(tuple(), float)
    assert darr.shape == nparr.shape
    assert darr.dtype == nparr.dtype
    assert_eq(darr, nparr)

    darr = da.indices((0,), float, chunks=(1,))
    nparr = np.indices((0,), float)
    assert darr.shape == nparr.shape
    assert darr.dtype == nparr.dtype
    assert_eq(darr, nparr)

    darr = da.indices((0, 1, 2), float, chunks=(1, 1, 2))
    nparr = np.indices((0, 1, 2), float)
    assert darr.shape == nparr.shape
    assert darr.dtype == nparr.dtype
    assert_eq(darr, nparr)
