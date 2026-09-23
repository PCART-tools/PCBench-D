def test_optimize():
    x = np.arange(5).astype('f4')
    a = da.from_array(x, chunks=(2,))
    expr = a[1:4] + 1
    result = optimize(expr.dask, expr.__dask_keys__())
    assert isinstance(result, dict)
    assert all(key in result for key in expr.__dask_keys__())
