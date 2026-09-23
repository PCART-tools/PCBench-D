def test_plan_rechunk_asymmetric():
    a = ((1,) * 1000, (80000000,))
    b = ((1000,), (80000,) * 1000)
    steps = plan_rechunk(a, b, itemsize=8)
    assert len(steps) > 1

    x = da.ones((1000, 80000000), chunks=(1, 80000000))
    y = x.rechunk((1000, x.shape[1] // 1000))
    assert len(y.dask) < 100000
