def test_slicing_integer_no_warnings():
    # https://github.com/dask/dask/pull/2457/
    X = da.random.random((100, 2), (2, 2))
    idx = np.array([0, 0, 1, 1])
    with pytest.warns(None) as rec:
        X[idx].compute()
    assert len(rec) == 0
