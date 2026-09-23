@pytest.mark.skipif(not hasattr(np,'broadcast_to'),
                    reason='requires numpy 1.10 method "broadcast_to"')
def test_array_broadcasting():
    arr = np.arange(6).reshape((2, 3))
    daones = da.ones((2, 3, 4), chunks=3)
    assert da.random.poisson(arr, chunks=3).compute().shape == (2, 3)

    for x in (arr, daones):
        y = da.random.normal(x, 2, chunks=3)
        assert y.shape == x.shape
        assert y.compute().shape == x.shape

    y = da.random.normal(daones, 2, chunks=3)
    assert set(daones.dask).issubset(set(y.dask))

    assert da.random.normal(np.ones((1, 4)),
                            da.ones((2, 3, 4), chunks=(2, 3, 4)),
                            chunks=(2, 3, 4)).compute().shape == (2, 3, 4)
    assert da.random.normal(scale=np.ones((1, 4)),
                            loc=da.ones((2, 3, 4), chunks=(2, 3, 4)),
                            size=(2, 2, 3, 4),
                            chunks=(2, 2, 3, 4)).compute().shape == (2, 2, 3, 4)

    with pytest.raises(ValueError):
        da.random.normal(arr, np.ones((3, 1)), size=(2, 3, 4), chunks=3)

    for o in (np.ones(100), da.ones(100, chunks=(50,)), 1):
        a = da.random.normal(1000 * o, 0.01, chunks=(50,))
        assert 800 < a.mean().compute() < 1200

    # ensure that mis-matched chunks align well
    x = np.arange(10)**3
    y = da.from_array(x, chunks=(1,))
    z = da.random.normal(y, 0.01, chunks=(10,))

    assert 0.8 < z.mean().compute() / x.mean() < 1.2
