def test_periodic():
    x = np.arange(64).reshape((8, 8))
    d = da.from_array(x, chunks=(4, 4))

    e = periodic(d, axis=0, depth=2)
    assert e.shape[0] == d.shape[0] + 4
    assert e.shape[1] == d.shape[1]

    assert_eq(e[1, :], d[-1, :])
    assert_eq(e[0, :], d[-2, :])
