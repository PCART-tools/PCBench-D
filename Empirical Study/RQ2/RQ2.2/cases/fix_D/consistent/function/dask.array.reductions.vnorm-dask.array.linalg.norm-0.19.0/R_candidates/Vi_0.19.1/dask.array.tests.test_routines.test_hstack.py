def test_hstack():
    x = np.arange(5)
    y = np.ones(5)
    a = da.arange(5, chunks=2)
    b = da.ones(5, chunks=2)

    assert_eq(np.hstack((x[None, :], y[None, :])),
              da.hstack((a[None, :], b[None, :])))
    assert_eq(np.hstack((x, y)), da.hstack((a, b)))
