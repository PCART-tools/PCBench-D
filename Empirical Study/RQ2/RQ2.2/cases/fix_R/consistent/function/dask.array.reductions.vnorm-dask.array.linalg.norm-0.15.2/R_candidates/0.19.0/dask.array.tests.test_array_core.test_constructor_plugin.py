def test_constructor_plugin():
    L = []
    L2 = []
    with dask.config.set(array_plugins=[L.append, L2.append]):
        x = da.ones(10, chunks=5)
        y = x + 1

    assert L == L2 == [x, y]

    with dask.config.set(array_plugins=[lambda x: x.compute()]):
        x = da.ones(10, chunks=5)
        y = x + 1

    assert isinstance(y, np.ndarray)
    assert len(L) == 2
