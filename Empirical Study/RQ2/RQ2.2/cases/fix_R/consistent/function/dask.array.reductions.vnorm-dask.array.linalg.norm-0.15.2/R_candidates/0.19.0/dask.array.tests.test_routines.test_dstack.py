def test_dstack():
    x = np.arange(5)
    y = np.ones(5)
    a = da.arange(5, chunks=2)
    b = da.ones(5, chunks=2)

    assert_eq(np.dstack((x[None, None, :], y[None, None, :])),
              da.dstack((a[None, None, :], b[None, None, :])))
    assert_eq(np.dstack((x[None, :], y[None, :])),
              da.dstack((a[None, :], b[None, :])))
    assert_eq(np.dstack((x, y)), da.dstack((a, b)))
