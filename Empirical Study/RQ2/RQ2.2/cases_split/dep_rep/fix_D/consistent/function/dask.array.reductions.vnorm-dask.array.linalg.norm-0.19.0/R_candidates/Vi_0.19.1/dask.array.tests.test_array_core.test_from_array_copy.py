def test_from_array_copy():
    # Regression test for https://github.com/dask/dask/issues/3751
    x = np.arange(10)
    y = da.from_array(x, -1)
    assert y.npartitions == 1
    y_c = y.copy()
    assert y is not y_c
    assert y.compute() is not y_c.compute()
