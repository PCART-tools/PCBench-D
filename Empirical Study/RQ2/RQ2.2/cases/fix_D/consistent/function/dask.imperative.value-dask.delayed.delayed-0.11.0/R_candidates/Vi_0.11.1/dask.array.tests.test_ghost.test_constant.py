def test_constant():
    x = np.arange(64).reshape((8, 8))
    d = da.from_array(x, chunks=(4, 4))

    e = constant(d, axis=0, depth=2, value=10)
    assert e.shape[0] == d.shape[0] + 4
    assert e.shape[1] == d.shape[1]

    assert_eq(e[1, :], np.ones(8, dtype=x.dtype) * 10)
    assert_eq(e[-1, :], np.ones(8, dtype=x.dtype) * 10)
