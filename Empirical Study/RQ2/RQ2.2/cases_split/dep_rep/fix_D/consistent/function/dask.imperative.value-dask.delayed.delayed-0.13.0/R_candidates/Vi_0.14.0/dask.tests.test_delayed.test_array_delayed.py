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

    task, dsk = to_task_dask(darr)
    orig = set(darr.dask)
    final = set(dsk)
    assert orig.issubset(final)
    diff = final.difference(orig)
    assert len(diff) == 1

    delayed_arr = delayed(darr)
    assert (delayed_arr.compute() == arr).all()
