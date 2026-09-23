def test_arange_float_step():
    darr = da.arange(2., 13., .3, chunks=4)
    nparr = np.arange(2., 13., .3)
    assert_eq(darr, nparr)

    darr = da.arange(7.7, 1.5, -.8, chunks=3)
    nparr = np.arange(7.7, 1.5, -.8)
    assert_eq(darr, nparr)

    darr = da.arange(0, 1, 0.01, chunks=20)
    nparr = np.arange(0, 1, 0.01)
    assert_eq(darr, nparr)

    darr = da.arange(0, 1, 0.03, chunks=20)
    nparr = np.arange(0, 1, 0.03)
    assert_eq(darr, nparr)
