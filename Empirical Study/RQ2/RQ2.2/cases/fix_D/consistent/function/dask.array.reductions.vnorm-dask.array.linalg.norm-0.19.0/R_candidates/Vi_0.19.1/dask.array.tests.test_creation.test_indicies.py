def test_indicies():
    darr = da.indices((1,), chunks=(1,))
    nparr = np.indices((1,))
    assert_eq(darr, nparr)

    darr = da.indices((1,), float, chunks=(1,))
    nparr = np.indices((1,), float)
    assert_eq(darr, nparr)

    darr = da.indices((2, 1), chunks=(2, 1))
    nparr = np.indices((2, 1))
    assert_eq(darr, nparr)

    darr = da.indices((2, 3), chunks=(1, 2))
    nparr = np.indices((2, 3))
    assert_eq(darr, nparr)
