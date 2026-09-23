def test_isnull_result_is_an_array():
    # regression test for https://github.com/dask/dask/issues/3822
    arr = da.from_array(np.arange(3, dtype=np.int64), chunks=-1)
    with ignoring(ImportError):
        result = da.isnull(arr[0]).compute()
        assert type(result) is np.ndarray
