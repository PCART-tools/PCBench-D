def test_array_delayed():
    np = pytest.importorskip('numpy')
    da = pytest.importorskip('dask.array')

    arr = np.arange(100).reshape((10, 10))
    darr = da.from_array(arr, chunks=(5, 5))
    val = delayed(sum)([arr, darr, 1])
    assert isinstance(val, Delayed)
    assert np.allclose(val.compute(), arr + arr + 1)
    assert val.sum().compute() == (arr + arr + 1).sum()
    assert val[0, 0].compute() == (arr + arr + 1)[0, 0]

    task, dasks = to_task_dasks(darr)
    assert len(dasks) == 1
    orig = set(darr.dask)
    final = set(dasks[0])
    assert orig.issubset(final)
    diff = final.difference(orig)
    assert len(diff) == 1
