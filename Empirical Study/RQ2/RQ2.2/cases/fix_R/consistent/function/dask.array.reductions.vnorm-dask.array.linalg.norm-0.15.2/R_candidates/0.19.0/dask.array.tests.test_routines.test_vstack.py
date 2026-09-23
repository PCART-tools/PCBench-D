def test_vstack():
    x = np.arange(5)
    y = np.ones(5)
    a = da.arange(5, chunks=2)
    b = da.ones(5, chunks=2)

    assert_eq(np.vstack((x, y)), da.vstack((a, b)))
    assert_eq(np.vstack((x, y[None, :])), da.vstack((a, b[None, :])))
