def test_slice_stop_0():
    # from gh-125
    a = da.ones(10, chunks=(10,))[:0].compute()
    b = np.ones(10)[:0]
    assert_eq(a, b)
